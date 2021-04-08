# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class ProductTemplate(models.Model):

    _inherit = 'product.template'
    #_inherit = 'barcode.rule'

    barcode_ids = fields.One2many(
        comodel_name="product.multi.barcode",
        compute="_compute_barcode_ids",
        inverse="_set_barcode_ids",
        string="Seriales"
    )

    qty_per_product = fields.Integer(
        string='Ingrese Cantidad'
    )


    @api.multi
    def generate_serie_barcode(self):
        self.ensure_one()
        self.product_variant_ids.generate_barcode()
        

    @api.onchange('barcode_rule_id')
    def onchange_barcode_rule_id(self):
        self.generate_type = self.barcode_rule_id.generate_type

    @api.multi
    def action_set_qty(self):
        self.ensure_one()
        self.barcode_ids.write({'name': self.qty_per_product})

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
        templates = super(ProductTemplate, self).create(vals)
        templates._re_write_barcode(vals)
        return templates

