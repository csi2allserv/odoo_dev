# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartnerUSA(models.Model):
    _inherit = 'res.partner'

    billable_expenses_ids = fields.One2many('billable.expenses', 'customer_id')
