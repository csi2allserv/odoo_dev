# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    John W. Viloria Amaris <john.viloria.amaris@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

def price_unit_calculate(list_price, currency, profit, trm, import_percentage):
    price_unit = 0.0
    try:
        if currency == 'usd':
            import_value = list_price * (float(import_percentage)/100)
            profit_value = (list_price + import_value) * (float(profit)/100)
            price_unit = (list_price + profit_value + \
                         import_value) * trm
        else:
            price_unit = list_price + list_price * (float(profit)/100)
    except:
        pass
    return price_unit

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_default_trm(self):
        try:
            return self.env['res.currency'].search(\
                [('name','in',('USD','usd'))])[0].rate
        except:
            return 0

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(SaleOrder, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return res

    trm = fields.Float('TRM', default=_get_default_trm, readonly=True)
    is_default_pricelist = fields.Boolean(related='pricelist_id.is_default')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(SaleOrderLine, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return res

    @api.multi
    @api.onchange('product_brand_id')
    def product_brand_id_change(self):
        if not self.product_brand_id:
            return
        brand_id = self.product_brand_id.id
        products = self.env['product.product'].\
            search([('product_brand_id','=',brand_id)])
        ids = [product.id for product in products]
        return {'domain':{'product_id':[('id','in',ids)]}}

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id.id,
                quantity=self.product_uom_qty,
                date_order=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            #Se reemplaza product.price_unit por self.tmp_price_unit, para evitar el
            #cambio del precio establecido manualmente.
            self.price_unit = self.env['account.tax']._fix_tax_included_price(self.tmp_price_unit, product.taxes_id, self.tax_id)

    def _get_default_trm(self):
        try:
            return self.env['res.currency'].search(\
                [('name','in',('USD','usd'))])[0].rate
        except:
            return 0

    order_trm = fields.Float(string='TRM', default=_get_default_trm, \
        readonly=True, help='TRM usada el dia de la cotización')
    profit_percentage = fields.Integer(string='Profit Percentage')
    import_percentage = fields.Integer(string='Import Percentage')
    currency = fields.Selection([
        ('cop', 'Colombian Peso'),
        ('usd', 'Dollar'),
        ('eur', 'Euro')
        ], string='Currency', default='cop')
    tmp_price_unit = fields.Float('Price Unit', default=0.0, \
        help='Precio del producto unitario y sin IVA')
    standard_price = fields.Float('Standard Price', default=0.0, \
        help='Costo del producto')
    list_price = fields.Float('List Price', default=0.0)
    product_brand_id = fields.Many2one('product.brand', string='Brand')
    pricelist_id = fields.Many2one(related='order_id.pricelist_id',\
        string='Pricelist')     #REQ #18
    pricelist_default = fields.Boolean('Is Default Pricelist?')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        res = super(SaleOrderLine, self).product_id_change()
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        price_unit = product.price
        standard_price = self.product_id.standard_price
        vals = {}
        vals['price_unit'] = price_unit
        vals['list_price'] = price_unit
        vals['tmp_price_unit'] = price_unit
        vals['standard_price'] = standard_price
        self.update(vals)
        return res

    @api.multi
    @api.onchange('import_percentage', 'profit_percentage',\
        'list_price','currency')
    def onchange_import_percentage(self):
        if not self.import_percentage and not self.profit_percentage \
            and not self.list_price:
            return
        vals = {}
        price_unit = False
        if self.product_id:
            vals['price_unit'] = price_unit
            vals['tmp_price_unit'] = price_unit
            self.update(vals)
            try:
                price_unit = price_unit_calculate(self.list_price,
                            self.currency, self.profit_percentage,
                            self._get_default_trm(), self.import_percentage
                            )
            except:
                pass
        vals['price_unit'] = price_unit
        vals['tmp_price_unit'] = price_unit
        self.update(vals)

#REQ #18
class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_default = fields.Boolean('Default Pricelist?', default=0)
#FIN REQ #18