# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError


class PrintProductBarcodes(models.TransientModel):
    _name = "prin_product"
    _description = 'Product Labels Barcodes'
    _inherit = 'product.template' 
    # TODO:  tests - try_report_action



    name = fields.Char('Barcode', required=True)

    barcode_ids = fields.One2many(
        comodel_name="prin_product",
        compute="_compute_barcode_ids",
        inverse="_set_barcode_ids",
        string="Multi Barcode"
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete='cascade'
    )
    active = fields.Boolean(
        related="product_id.active",
        default=True,
        readonly=False,
        store=True)
    _sql_constraints = [
        ('uniq_multi_barcode_name', 'unique(name)',
         'Multi barcode should be unique for each product. '
         'Please check again!.'),
    ]

    @api.constrains('name')
    def check_uniqe_name(self):
        for rec in self:
            domain = [
                ('barcode', '=', rec.name),
                ('id', '!=', rec.product_id.id)
            ]
            products = self.env['product.product'].search(domain)
            if products:
                raise UserError(
                    'Multi barcode should be unique !.'
                    'There is an same barcode on products (ids:%s) form.'
                    ' Please check again !' %
                    ','.join(map(lambda x: str(x), products.ids)))

    @api.depends('product_variant_ids', 'product_variant_ids.barcode_ids')
    def _compute_barcode_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.barcode_ids = p.product_variant_ids.barcode_ids

    def _set_barcode_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.product_variant_ids.barcode_ids = p.barcode_ids

    def _re_write_barcode(self, vals):
        barcode_vals = vals.get('barcode_ids')
        if barcode_vals:
            for template in self:
                if len(template.product_variant_ids) == 1:
                    template.product_variant_ids.write({
                        'barcode_ids': barcode_vals
                    })

    @api.model
    def create(self, vals):
        templates = super(PrintProductBarcodes, self).create(vals)
        templates._re_write_barcode(vals)
        return templates