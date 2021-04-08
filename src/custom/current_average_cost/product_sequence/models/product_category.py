# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    code_prefix = fields.Char(
        string="Prefijo de Referencia",
        help="Prefijo utilizado para generar la referencia interna para productos "
             "creado con esta categoría. Si está en blanco el "
             "se usará la secuencia predeterminada.",
    )
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence", string="Product Sequence",
        help="Este campo contiene la información relacionada con la numeración "
             "de los asientos de este diario.",
        copy=False, readonly=True,
    )

    @api.model
    def _prepare_ir_sequence(self, prefix):
        """Prepare los vals para crear la secuencia.
        : prefijo param: una cadena con el prefijo de la secuencia.
        : return: un dict con los valores..
        """
        vals = {
            "name": "Product " + prefix,
            "code": "product.product - " + prefix,
            "padding": 5,
            "prefix": prefix,
            "company_id": False,
        }
        return vals

    @api.multi
    def write(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            for rec in self:
                if rec.sequence_id:
                    rec.sudo().sequence_id.prefix = prefix
                else:
                    seq_vals = self._prepare_ir_sequence(prefix)
                    rec.sequence_id = self.env["ir.sequence"].create(seq_vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            seq_vals = self._prepare_ir_sequence(prefix)
            sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().create(vals)
