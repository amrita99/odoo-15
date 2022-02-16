from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    customer_tag = fields.Many2many('res.partner.category', related='partner_id.category_id',string='Customer Tag')

    @api.model
    def create(self, vals):
        print(vals)
        if not vals.get('customer_tag'):
            partner_id = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
            if partner_id.category_id:
                vals['customer_tag'] = partner_id.category_id.name
        result = super(SaleOrder, self).create(vals)
        return result

