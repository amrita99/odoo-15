from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    dob = fields.Date(string='DOB', required=True)
    customer_age = fields.Integer(string='Age', compute='get_age_from_customer', store=True)

    @api.depends('dob')
    def get_age_from_customer(self):
        for record in self:
            if record.dob:
                customer_age = relativedelta(date.today(), record.dob).years
                record.customer_age = customer_age
    # def get_age_from_customer(self):
        # for record in self:
        #     if record.dob:
        #         dt = date.today()
        #         dob = record.dob
        #         dt3 = relativedelta(dt, dob)
        #         record.customer_age = dt3.years

     #
     # def get_age_from_customer(self):
     #    for record in self:
     #        if record.dob:
     #            customer_age = relativedelta(date.today(), record.dob).year
     #            record.customer_age = customer_age






