from odoo import _, api, fields, models


class SaleReplace(models.Model):
    _inherit = 'product.product'
    dummy_product = fields.Boolean(strings="Dummy Product")


class SaleDummy(models.Model):
    _inherit = 'purchase.order.line'

    dummy_product = fields.Boolean(strings="Dummy Product", related='product_id.dummy_product')

    def replace_product(self):
        form_view = [(self.env.ref('sale_custom.create_replace_button').id, 'form')]
        view_id = self.env.ref('sale_custom.create_replace_button').id
        print("entered here")
        print(self.order_id.name, "self.order_id.name")
        return {
            'type': 'ir.actions.act_window',
            'name': _("Replace Wizard"),
            'res_model': 'create.replace.button',
            'view_mode': 'form',
            'views': form_view,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_name': self.order_id.name,
                'default_purchase_order_line': self.id,
            }
        }


