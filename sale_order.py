from odoo import api, fields, models
import base64
import io
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    customer_tag = fields.Many2many('res.partner.category', related='partner_id.category_id',string='Customer Tag')


    @api.constrains('validity_date')
    def _check_validity_date(self):
        for record in self:
            if record.validity_date < fields.Date.today():
                raise ValidationError("The expiration date cannot be set in the past")

    def action_confirm(self):

        super(SaleOrder, self).action_confirm()
        # pdf = self.env['sale.order'].sudo().get_pdf([invoice.id], 'account.report_invoice')
        pdf = self.env.ref('sale.action_report_saleorder')._render_qweb_pdf(self.ids)
        self.env['ir.attachment'].create({
            'name': self.name + '.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf[0]),
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/x-pdf'

        })

        return self.env.ref('sale.action_report_saleorder').report_action(self)

    @api.model
    def create(self, vals):
        print(vals)
        if not vals.get('customer_tag'):
            partner_id = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
            if partner_id.category_id:
                vals['customer_tag'] = partner_id.category_id.name
        result = super(SaleOrder, self).create(vals)
        return result



