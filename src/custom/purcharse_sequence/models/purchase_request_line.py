# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file
# for full copyright and licensing details.

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'purchase.request.line'

    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product'
    )