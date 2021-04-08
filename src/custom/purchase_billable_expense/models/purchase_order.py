# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class PurchaseOrderUSA(models.Model):
    _inherit = 'purchase.order'

    billable_expenses_ids = fields.One2many('billable.expenses', 'purchase_id')  # correspond with each purchase line

    def open_expense_popup(self):
        # check if expense has been created for a bill line yet?
        expense_ids = set(expense.purchase_line_id.id for expense in self.billable_expenses_ids)
        for line in self.order_line:
            if line.id not in expense_ids:
                date = datetime.strptime(fields.Datetime.to_string(self.date_order), DEFAULT_SERVER_DATETIME_FORMAT)
                self.env['billable.expenses'].sudo().create({'purchase_id': self.id,
                                                             'purchase_line_id': line.id,
                                                             'description': line.name,
                                                             'amount': line.price_subtotal,
                                                             'bill_date': date})
        # open popup
        view_id = self.env.ref('purchase_billable_expense.purchase_assign_expense_popup_form').id
        return {
            'name': 'Assign a customer to any billable expense',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'target': 'new',
            'res_id': self.id,
            'view_id': view_id,
        }

    def assign_customer(self):
        return {'type': 'ir.actions.act_window_close'}

    def button_cancel(self):
        """
        Remove Expense if Purchase is canceled/deleted.
        """
        res = super(PurchaseOrderUSA, self).button_cancel()
        for record in self:
            record.billable_expenses_ids.sudo().unlink()  # delete expense for PO

        return res


class PurchaseOrderLineUSA(models.Model):
    _inherit = 'purchase.order.line'

    usa_description = fields.Text('Description', compute='_get_usa_description',
                                  inverse='_set_usa_description', store=True)
    billable_expenses_ids = fields.One2many('billable.expenses', 'purchase_line_id')  # only one record, for PO
    invoiced_to_id = fields.Many2one('account.invoice', compute='_get_usa_description', store=True)

    @api.depends('name', 'billable_expenses_ids', 'billable_expenses_ids.customer_id',
                 'billable_expenses_ids.is_outstanding', 'state')
    def _get_usa_description(self):
        for record in self:
            record.usa_description = record.name

            if record.state in ['purchase', 'done']:
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
            if record.state not in ['purchase', 'done']:
                record.name = record.usa_description

    @api.onchange('usa_description')
    def _on_change_usa_description(self):
        """
        We need this one since Inverse func only runs when Save
        """
        for record in self:
            if record.state not in ['purchase', 'done']:
                record.name = record.usa_description

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
