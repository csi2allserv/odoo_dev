from odoo import api, fields, models



_GENERATE_TYPE = [
    ('no', 'No'),
    ('secuence', 'Generar secuencia'),
]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    generate_serie = fields.Selection( string='Generar serie', selection=_GENERATE_TYPE,
                                      help = 'Si desea generar serie de codigo de barras seleccione Secuencia' )
    barcode_ids = fields.One2many(
        comodel_name="prin_product",
        compute="_compute_barcode_ids",
        inverse="_set_barcode_ids",
        string="Multi Barcode"
    )

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