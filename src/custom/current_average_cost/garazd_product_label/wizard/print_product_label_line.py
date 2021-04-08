# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PrintProductLabelLine(models.TransientModel):
    _name = "print.product.label.line"
    _description = 'Line with Product Label Data'
   
   
    selected = fields.Boolean(
        string='Imprimir',
        # compute='_compute_selected',
        readonly=False,
        default=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    wizard_id = fields.Many2one('print.product.label', 'Print Wizard')
    product_id = fields.Many2one('product.template', 'Product', required=True)
    barcode = fields.Char('Barcode', related='product_id.barcode')
    qty_initial = fields.Integer('Initial Qty', default=1)
    qty = fields.Integer('Label Qty', default=1)

    @api.multi
    def action_plus_qty(self):
        for record in self:
            record.update({'qty': record.qty + 1})
            if record.qty > 0:
                record.selected = True

    @api.multi
    def action_minus_qty(self):
        for record in self:
            if record.qty > 0:
                record.update({'qty': record.qty - 1})
            if record.qty <= 0:
                record.selected = False
