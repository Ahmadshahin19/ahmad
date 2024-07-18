from odoo import models, fields


class SaleOrder(models.Model): # عملنا انهيرت لمديول المبيعات مشان نضيف عليه حقول او نعدل الاجراءات الخاصين به
    _inherit = 'sale.order'


    property_id = fields.Many2one('property')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print('inherit sales order')
        #self.partner_id = False # هيك اذا بدنا نوقف لاجراء بسبب خطا عم وجود عميل
        return res