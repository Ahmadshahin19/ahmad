from odoo import models


class Owner(models.Model): # عملنا انهيرت لمديول owner بهي الطريقة بانشئ جدول جديد بيحتوي على كامل الحقول والاجراءات الموجودة في المديول الانهيرت
    _name = 'client'
    _inherit = 'owner'