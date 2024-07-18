from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _rec_name = 'no' # هاد مشان يغير الحقل يلي على اسمه بيتسمى السجل بالاعلى عند فتح الفورم

    _inherit = ['mail.thread','mail.activity.mixin'] # عملنا انهيرت لمديولين مشان التشات

    name = fields.Char(required=True, size=3) #size بخليك تكتب عدد معين من الحروف يستخدم في النصوص فقط وليس الارقام
    no = fields.Char()
    description = fields.Text(groups="app_one.property_manager_group")
    date = fields.Date(tracking=True) # حطينا tracking مسان يصير يظهر التغيير في الرسائل يلي في التشات
    integer = fields.Integer()
    float = fields.Float(default=45,digits=(0, 4)) # digitsبيعدل عدد الفواصل العشرية
    float2 = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=True)
    date_time = fields.Datetime()
    bool3 = fields.Boolean()
    selection = fields.Selection([
        ('north','North'),
        ('south','South'),
    ],default='north')
    owner_id = fields.Many2one('owner')
    owner_address = fields.Char(related='owner_id.address', readonly=False, store=True)
    owner_phone = fields.Char(related='owner_id.phone')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft','Draft'),
        ('post','Post'),
        ('cancel','Cancel'),
        ('closed', 'Closed'),
    ], default='draft')
    line_ids = fields.One2many('property.line','property_id')
    active = fields.Boolean(default=True) # عند وضع هذا الحقل يصبح بالامكان استخدام ميزة الارشفة وضفنا في البحث فلتر من اجل اظهار المؤرشف
    expected_selling_date = fields.Date(tracking=True)
    is_late = fields.Boolean()
    ref = fields.Char(default='New')
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_copute_next_time')

    _sql_constraints = [ # بتعمل حقل الاسم فريد لا يمكن تكراره وبتظهر في pgadmin فيconstraints تحت الجداول
        ('unique_name','unique("name")','This name is exist')
    ]

    @api.constrains('integer') #عند انشاء لحقل اول مرة او عند تغير قيمته يعمل هذا الاجراء لحقلinteger
    def _check_integer_greater_zero(self):
        for rec in self:
            if rec.integer == 0:
                raise ValidationError('Please add valid number of Integer')

     #ملاحظة هدول اجراءات موجودين في الموديل عملنالهن انهيرت بهي الطريقة وعدلنا عليهن بانو يطبع شي او ممكن ننفذ اجراء اول وبعدين ينفذ الاجراء الرئيسي write و  create وunlink
    @api.model_create_multi #بتنفذ اجراء معين عند انشاء سجل جديد ولكن هون خليناها بس تطلع في التيرمنال انو تم انشاء سجل
    def create(self, vals):
        res = super(Property,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        #print('create')
        return res

    @api.model #بتنفذ اجراء معين عند رؤية سجل ولكن هون خليناها بس تطلع في التيرمنال انو تم انشاء سجل
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property,self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        #print('read')
        return res

    def write(self, vals): #بتنفذ اجراء معين عند تعديل سجل ولكن هون خليناها بس تطلع في التيرمنال انو تم انشاء سجل
        res = super(Property,self).write(vals)
        #print('write')
        return res

    def unlink(self): #بتنفذ اجراء معين عند حذف سجل ولكن هون خليناها بس تطلع في التيرمنال انو تم انشاء سجل
        res = super(Property,self).unlink()
        #print('unlink')
        return res

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_post(self):
        for rec in self:
            rec.create_history_record(rec.state, 'post')
            rec.write({
                'state': 'post'
            })

    def action_cancel(self):
        for rec in self:
            rec.create_history_record(rec.state, 'cancel') # الكود الخاص باشاء الحالة القديمة والجديدة في مديول الهيستوري
            rec.state = 'cancel'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    @api.onchange('float','float2','owner_id') #تستخدم عند تغير قيمة حقل موجود في العرض ولا تتاثر بالحقول غير الموجودة في العرض ولا تقبل العلاقات من حقول خارجية
    def _onchange_float_or_float2(self):
        for rec in self:
            #rec.diff = rec.float + rec.float2
            #print(rec)
            #print("onchange_float_or_float2")

            if rec.float > 10 : # هذه بتظهر تنبيه للمستخدم ولكن لا توقفه فقط تحذير
                return {
                    'warning':{'title': 'warning', 'message': 'Float great than 10', 'type': 'notification'}
                }


    @api.depends('create_time')
    def _copute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    @api.depends('float', 'float2', 'owner_id.phone') #تستخدم في حال تغير الحقول حتى لو كاتن غير موجودة في العرض وايضا تقبل العلاقات مع الحقول من موديولات اخرى مثلowner_id.phone فعند تغير phone يعمل الاجراء ايضا ولكن عند تضارب الاكواد مع onchange يتعطلdepends ويعمل onchange فهي اقوى
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.float - rec.float2
            #print(rec)
            #print("diff_depends")

    def create_history_record(self, old_state, new_state, reason=""): # هذا الاجراء بخلينا ننشى حقول في مديول ثاني ويحط اليوزر الحالي والبروبرتي الحالي والحالة القديمة والجديدة عن طريق كود ضفناه في الاجراءات فوق مع كل اجراء بغير الحالة وحطينة reason="" مشان فوق لما فعلنا الاجراء عند تغير الحالة ما حطينا متغير reason مشان ما يصير خطئ اذا مافي reason بياخد فراغ
        for rec in self:
            # مهم جدا هون استخدمنا طريقة حلوة بتانشئ حقول في لاين الهيستوري في الهيستوري وبتحط الايدي تبعها في lin_ids
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids]
            })

    def action_open_change_state_wizard(self):  #هذه من اجل فتح ويزارد مديول ثاني عن طريق المعرف الخارجي للاكشن ويندوز قي مديول الاكشن ملاحظةxml_id هو حقل في الاكشن _for_ تشبه السيرش لهاد الحقل
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_relate_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()