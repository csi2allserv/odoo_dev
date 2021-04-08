

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    barcode_ids = fields.One2many(
        comodel_name="prin_product",
        inverse_name="product_id",
        string="Codigos de Barras "
    )

    @api.model
    def compute_multi_barcode_product_domain(self, args):
        """
        :param args: original args
        :return: new arguments that allow search more multi barcode object
        """
        domain = []
        for arg in args:
            if isinstance(arg, (list, tuple)) and arg[0] == 'barcode':
                domain += ['|', ('barcode_ids.name', arg[1], arg[2]), arg]
            else:
                domain += [arg]
        return domain

    @api.model
    def _search(self, args, offset=0, limit=None,
        order=None, count=False, access_rights_uid=None):

        new_args = self.compute_multi_barcode_product_domain(args)
        return super(ProductProduct, self)._search(
            new_args, offset, limit, order, count,
            access_rights_uid
        )

    @api.model
    def create(self, vals):
        return super(ProductProduct, self).create(vals)

    @api.constrains('barcode')
    def check_uniqe_name(self):
        for rec in self:
            domain = [('name', '=', rec.barcode)]
            barcodes = self.env['product.multi.barcode'].search(domain)
            if barcodes:
                product_ids = barcodes.mapped('product_id').ids
                raise UserError(
                    'Multi barcode should be unique !.'
                    'There is an same barcode on multi-barcode tab of products (ids:%s).'
                    ' Please check again !' %
                    ','.join(map(lambda x: str(x), product_ids)))
