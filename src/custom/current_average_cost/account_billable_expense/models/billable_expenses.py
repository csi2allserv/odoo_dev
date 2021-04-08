# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.misc import formatLang


class BillableExpenses(models.Model):
    _name = 'billable.expenses'
    _description = 'Billable Expenses'
    _rec_name = 'description'

    bill_id = fields.Many2one('account.invoice')
    bill_line_id = fields.Many2one('account.invoice.line')  # expense created from a bill line
    description = fields.Text('Description')
    amount = fields.Monetary('Amount')
    bill_date = fields.Date('Date')

    currency_id = fields.Many2one('res.currency', compute='_compute_company_id', store=True, string='Expense Currency')
    company_id = fields.Many2one('res.company', compute='_compute_company_id', store=True)
    customer_id = fields.Many2one('res.partner', 'Customer')

    invoice_line_id = fields.Many2one('account.invoice.line')  # expense added to an invoice line
    is_outstanding = fields.Boolean('Outstanding', compute='_get_outstanding_state', store=True)

    # Express in Invoice currency
    invoice_currency_id = fields.Many2one('res.currency', string='Invoice Currency')
    amount_currency = fields.Monetary('Amount Currency', compute='_get_amount_currency', store=True)

    # for report
    source_document = fields.Char('Source Document', compute='_compute_company_id', store=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', compute='_compute_company_id', store=True)

    @api.depends('invoice_line_id', 'invoice_line_id.invoice_id.state')
    def _get_outstanding_state(self):
        for record in self:
            if not record.invoice_line_id or (record.invoice_line_id and
                                              record.invoice_line_id.invoice_id.state == 'draft'):
                record.is_outstanding = True
            else:
                record.is_outstanding = False

    @api.depends('bill_id')
    def _compute_company_id(self):
        for record in self:
            bill = record.bill_id
            if bill:
                record.source_document = bill.number
                record.supplier_id = bill.partner_id
                record.currency_id = bill.currency_id
                record.company_id = bill.company_id

    @api.depends('amount', 'currency_id', 'invoice_currency_id')
    def _get_amount_currency(self):
        for record in self:
            if record.invoice_currency_id:
                record.amount_currency = record.currency_id._convert(record.amount, record.invoice_currency_id,
                                                                     record.company_id, fields.Date.today())
            else:
                record.amount_currency = record.amount

    def _get_log_msg(self, vals):
        current_customer = self.customer_id
        new_customer = self.env['res.partner'].browse(vals['customer_id'])
        formatted_amount = formatLang(self.env, self.amount, currency_obj=self.currency_id)

        if not new_customer:  # remove case
            msg = 'Billable expense %s %s removed' % (self.description, formatted_amount)
        else:
            customer_link = '<a href=javascript:void(0) data-oe-model=res.partner data-oe-id=%d>%s</a>' % \
                            (new_customer.id, new_customer.name)
            if not current_customer:  # assign
                msg = 'Billable expense %s %s assigned to %s' % \
                      (self.description, formatted_amount, customer_link)
            else:  # re-assign
                msg = 'Billable expense %s %s re-assigned to %s' % \
                      (self.description, formatted_amount, customer_link)

        return msg

    def _log_message_expense(self, vals):
        """
        Split into different function so we can inherit purchase_billable_expense
        """
        for record in self:
            msg = record._get_log_msg(vals)
            record.bill_id.message_post(body=msg, subtype='account_billable_expense.mt_billable_expense')

    @api.multi
    def write(self, vals):
        if 'customer_id' in vals:
            vals['invoice_line_id'] = False  # reassign expense for another customer
            self._log_message_expense(vals)

        res = super(BillableExpenses, self).write(vals)

        return res
