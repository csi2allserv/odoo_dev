# -*- coding: utf-8 -*-

from odoo import api, fields, models


class BillableExpenses(models.Model):
    _inherit = 'billable.expenses'

    purchase_id = fields.Many2one('purchase.order')
    purchase_line_id = fields.Many2one('purchase.order.line')  # expense created from a PO line

    @api.depends('purchase_id', 'bill_id')
    def _compute_company_id(self):
        """
        Override to get data from PO
        """
        for record in self:
            bill = record.bill_id
            purchase = record.purchase_id
            if bill:
                record.source_document = bill.number
                record.supplier_id = bill.partner_id
                record.currency_id = bill.currency_id
                record.company_id = bill.company_id
            elif purchase:
                record.source_document = purchase.name
                record.supplier_id = purchase.partner_id
                record.currency_id = purchase.currency_id
                record.company_id = purchase.company_id

    def _log_message_expense(self, vals):
        """
        Override to log note in PO
        """
        for record in self:
            msg = record._get_log_msg(vals)
            if record.bill_id:
                record.bill_id.message_post(body=msg, subtype='account_billable_expense.mt_billable_expense')
            elif record.purchase_id:
                record.purchase_id.message_post(body=msg, subtype='account_billable_expense.mt_billable_expense')
