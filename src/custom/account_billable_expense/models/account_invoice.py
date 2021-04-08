# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoiceUSA(models.Model):
    _inherit = 'account.invoice'

    billable_expenses_ids = fields.One2many('billable.expenses', 'bill_id')  # correspond with each invoice line
    expense_btn_name = fields.Char(compute='_get_expense_btn_name')
    is_billable = fields.Boolean('Billable expense', compute='_get_is_billable', store=True)  # to set condition on view

    @api.depends('invoice_line_ids', 'invoice_line_ids.is_billable')
    def _get_is_billable(self):
        for record in self:
            record.is_billable = any(line.is_billable for line in record.invoice_line_ids)

    def _get_expense_btn_name(self):
        for record in self:
            expenses = record.partner_id.billable_expenses_ids.filtered(lambda ex: ex.is_outstanding
                                                                                   and ex.company_id == self.env.user.company_id)
            if expenses:
                added_expenses = expenses.filtered(lambda ex: ex.invoice_line_id)
                if not added_expenses:
                    record.expense_btn_name = '%s billable expense(s) can be added' % len(expenses)
                else:
                    record.expense_btn_name = '%s of %s billable expense(s) added' \
                                              % (len(added_expenses), len(expenses))
            else:
                record.expense_btn_name = False

    @api.onchange('partner_id')
    def _update_expense_btn_name(self):
        if self.type == 'out_invoice':
            self._get_expense_btn_name()
            billable_lines = self.invoice_line_ids.filtered(lambda x: x.is_billable)
            return {
                'value': {'invoice_line_ids': [(2, x.id) for x in billable_lines]}
            }

    def get_customer_billable_expenses(self):
        billable_expense = self.partner_id.billable_expenses_ids.filtered(lambda ex: ex.is_outstanding
                                                                         and ex.company_id == self.env.user.company_id)

        billable_expense.write({'invoice_currency_id': self.currency_id.id})
        return billable_expense.ids

    def open_expense_popup(self):
        # check if expense has been created for a bill line yet?
        expense_ids = set(expense.bill_line_id.id for expense in self.billable_expenses_ids)
        for line in self.invoice_line_ids:
            if line.id not in expense_ids:
                self.env['billable.expenses'].sudo().create({'bill_id': self.id,
                                                             'bill_line_id': line.id,
                                                             'description': line.name,
                                                             'amount': line.price_subtotal,
                                                             'bill_date': self.date_invoice})
        # open popup
        view_id = self.env.ref('account_billable_expense.assign_expense_form').id
        return {
            'name': 'Assign a customer to any billable expense',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'target': 'new',
            'res_id': self.id,
            'view_id': view_id,
        }

    def assign_customer(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """
        Remove Expense if Bill is canceled/deleted.
        Bill has to be canceled first in order to be deleted, so don't need to implement unlink.
        """
        res = super(AccountInvoiceUSA, self).action_cancel()
        for record in self:
            record.billable_expenses_ids.sudo().unlink()  # delete expense for bill

            # make expense available again for invoice
            for line in record.invoice_line_ids:
                reset_expenses = line.invoice_billable_expenses_ids.filtered(lambda x: x.invoice_line_id.id == line.id)
                reset_expenses.sudo().write({'invoice_line_id': False})
                line.invoice_billable_expenses_ids = [(5,)]

        return res

    def from_expense_to_invoice(self, values, mode):
        # get default account_id
        journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1) # customer invoice
        account_id = journal_id.default_credit_account_id.id  # invoice => credit_account

        expense_ids = self.env['billable.expenses'].browse(values)
        if mode == 'one':
            description = '\n'.join(expense.description for expense in expense_ids)
            amount = sum(expense.amount_currency for expense in expense_ids)
            source_list = expense_ids.mapped('source_document')
            source = ', '.join(source_list) if source_list else ''

            invoice = self.env['account.invoice.line'].create({'invoice_id': self.id,
                                                               'account_id': account_id,
                                                               'name': description,
                                                               'price_unit': amount,
                                                               'source_document': source,
                                                               'invoice_billable_expenses_ids': [(6, 0, values)]})
            expense_ids.sudo().write({'invoice_line_id': invoice.id})
        elif mode == 'item':
            for expense in expense_ids:
                invoice = self.env['account.invoice.line'].create({'invoice_id': self.id,
                                                                   'account_id': expense.bill_line_id and expense.bill_line_id.account_id.id or account_id,
                                                                   'name': expense.description,
                                                                   'price_unit': expense.amount_currency,
                                                                   'source_document': expense.source_document,
                                                                   'invoice_billable_expenses_ids': [(4, expense.id)]})
                expense.sudo().write({'invoice_line_id': invoice.id})
        return True


class AccountInvoiceLineUSA(models.Model):
    _inherit = 'account.invoice.line'

    type = fields.Selection(related='invoice_id.type')
    usa_description = fields.Text('Description', compute='_get_usa_description',
                                  inverse='_set_usa_description', store=True)
    is_billable = fields.Boolean('Billable expense', compute='_get_is_billable', store=True)
    billable_expenses_ids = fields.One2many('billable.expenses', 'bill_line_id')  # only one record, for bill

    # maybe more than one record, multi expenses added as one line
    invoice_billable_expenses_ids = fields.Many2many('billable.expenses')
    invoiced_to_id = fields.Many2one('account.invoice', compute='_get_usa_description', store=True)
    source_document = fields.Char('Source Document')

    @api.depends('name', 'billable_expenses_ids', 'billable_expenses_ids.customer_id',
                 'billable_expenses_ids.is_outstanding',
                 'invoice_id.state')
    def _get_usa_description(self):
        for record in self:
            record.usa_description = record.name

            if record.invoice_id.state in ['open', 'paid']:
                if record.billable_expenses_ids and record.billable_expenses_ids[0].customer_id:
                    expense = record.billable_expenses_ids[0]
                    if not expense.is_outstanding:  # already invoiced
                        record.invoiced_to_id = expense.invoice_line_id.invoice_id
                        bill_text = '\nInvoiced to %s\n%s' % \
                                    (expense.customer_id.name, record.invoiced_to_id.number)
                        record.usa_description = record.name + bill_text
                    else:
                        bill_text = '\nBillable expense for %s' % expense.customer_id.name
                        record.usa_description = record.name + bill_text

    def _set_usa_description(self):
        for record in self:
            if record.invoice_id.state not in ['open', 'paid']:
                record.name = record.usa_description

    @api.onchange('usa_description')
    def _on_change_usa_description(self):
        """
        We need this one since Inverse func only runs when Save
        """
        for record in self:
            if record.invoice_id.state not in ['open', 'paid']:
                record.name = record.usa_description

    @api.depends('invoice_billable_expenses_ids')
    def _get_is_billable(self):
        for record in self:
            record.is_billable = True if record.invoice_billable_expenses_ids else False

    def open_invoice_expense(self):
        view_id = self.env.ref('account.invoice_form').id
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'target': 'current',
            'res_id': self.invoiced_to_id.id,
            'view_id': view_id,
        }
