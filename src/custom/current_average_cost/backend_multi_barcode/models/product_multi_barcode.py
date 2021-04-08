# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductMultiBarcode(models.Model):

    _name = 'product.multi.barcode'

    name = fields.Char('Barcode', required=True)
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

                    
