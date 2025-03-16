from odoo import models, api

class FunctionModel(models.AbstractModel):
    _name = 'function.model'

    @api.model
    def get_action_value(self, view_id, user_id, external_module, external_id):

        view = self.env['ir.ui.view'].sudo().browse(view_id)
        user = self.env['res.users'].sudo().browse(user_id)

        if view.model == 'res.partner' and not user.has_group(external_module + '.' + external_id):
            return True
        return False