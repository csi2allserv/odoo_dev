# -*- coding: utf-8 -*-

from openerp import fields, models

class ProductProduct(models.Model):
    _inherit = "product.template"

    # REQ No. 105
    name = fields.Char('Name', required=True, translate=False, select=True)
    #END REQ 105

    tags_id = fields.Many2many('product.tag', 'product_tag_rel', \
        'prod_id', 'tag_id', string='Product tags')

class ProductTags(models.Model):
    _name = 'product.tag'

    name = fields.Char('Tag Name')

class ProductCategory(models.Model):
    _inherit = "product.category"

    is_electronic = fields.Boolean('Electronic System', default=False)
    is_metalworking = fields.Boolean('Metalworking Equipment', default=False)
