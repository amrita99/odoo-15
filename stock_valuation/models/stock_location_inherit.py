from odoo import fields, models, _
from odoo.exceptions import UserError


class InheritStockLocation(models.Model):
    _inherit = "stock.location"

    stock_valuation_account_id = fields.Many2one('account.account', string="Stock Valuation Account")
    stock_input_account_id = fields.Many2one('account.account', string="Stock Input Account")
    stock_output_account_id = fields.Many2one('account.account', string="Stock Output Account")


class InheritStockMove(models.Model):
    _inherit = "stock.move"

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        # This method returns a dictionary to provide an easy extension hook to modify the valuation lines (see purchase for an example)
        self.ensure_one()

        if self.location_dest_id.usage == 'internal':
            debit_line_account_id = self.location_dest_id.stock_valuation_account_id.id
            credit_line_account_id = self.location_dest_id.stock_input_account_id.id

            debit_line_vals = {
                'name': description,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'debit': debit_value if debit_value > 0 else 0,
                'credit': -debit_value if debit_value < 0 else 0,
                'account_id': debit_line_account_id,
            }

            credit_line_vals = {
                'name': description,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': credit_value if credit_value > 0 else 0,
                'debit': -credit_value if credit_value < 0 else 0,
                'account_id': credit_line_account_id,
            }

            rslt = {'credit_line_vals': credit_line_vals, 'debit_line_vals': debit_line_vals}

            if credit_value != debit_value:
                # Price Difference Account
                price_diff_account = self.product_id.property_account_creditor_price_difference
                if not price_diff_account:
                    price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
                if not price_diff_account:
                    raise UserError(
                        _('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))

                # Calculate price difference
                diff_amount = debit_value - credit_value

                rslt['price_diff_line_vals'] = {
                    'name': self.name,
                    'product_id': self.product_id.id,
                    'quantity': qty,
                    'product_uom_id': self.product_id.uom_id.id,
                    'ref': description,
                    'partner_id': partner_id,
                    'credit': diff_amount > 0 and diff_amount or 0,
                    'debit': diff_amount < 0 and -diff_amount or 0,
                    'account_id': price_diff_account.id,
                }

            return rslt
        else:
            debit_line_account_id = self.location_id.stock_output_account_id.id
            credit_line_account_id = self.location_id.stock_valuation_account_id.id

            debit_line_vals = {
                'name': description,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'debit': debit_value if debit_value > 0 else 0,
                'credit': -debit_value if debit_value < 0 else 0,
                'account_id': debit_line_account_id,
            }

            credit_line_vals = {
                'name': description,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                'ref': description,
                'partner_id': partner_id,
                'credit': credit_value if credit_value > 0 else 0,
                'debit': -credit_value if credit_value < 0 else 0,
                'account_id': credit_line_account_id,
            }

            rslt = {'credit_line_vals': credit_line_vals, 'debit_line_vals': debit_line_vals}

            if credit_value != debit_value:
                # Price Difference Account
                price_diff_account = self.product_id.property_account_creditor_price_difference
                if not price_diff_account:
                    price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
                if not price_diff_account:
                    raise UserError(
                        _('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))

                # Calculate price difference
                diff_amount = debit_value - credit_value

                rslt['price_diff_line_vals'] = {
                    'name': self.name,
                    'product_id': self.product_id.id,
                    'quantity': qty,
                    'product_uom_id': self.product_id.uom_id.id,
                    'ref': description,
                    'partner_id': partner_id,
                    'credit': diff_amount > 0 and diff_amount or 0,
                    'debit': diff_amount < 0 and -diff_amount or 0,
                    'account_id': price_diff_account.id,
                }

            return rslt
        return super(InheritStockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value,
                                                                            debit_account_id, credit_account_id,
                                                                            description)
