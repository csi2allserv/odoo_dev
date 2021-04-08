# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):

    _inherit = 'product.product'

    barcode_ids = fields.One2many(
        comodel_name="product.multi.barcode",
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
'''
    @api.model
    def create_barcode(self, vals):
        res = super(ProductProduct, self).create(vals)
        ean = generate_ean(str(res.id))
        res.barcode_ids = ean
        return res

    @api.multi
    def write(self, values):
        ean = generate_ean(str(self.product_tmpl_id.id))
        values['barcode_ids'] = ean
        return super(ProductProduct, self).write(values)

@api.multi
def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    """returns True if eancode is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])



def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))'''