# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductProductAppendSo(models.TransientModel):
    _name = 'product.product.append.so'

    order_id = fields.Many2one('sale.order')
    so_company_id = fields.Many2one('res.company', related='order_id.company_id', readonly=True)
    so_currency_id = fields.Many2one('res.currency', related='order_id.currency_id', readonly=True)
    product_uom_qty = fields.Float(string='Quantity', default=1.0)
    product_template_id = fields.Many2one('product.template')
    product_id = fields.Many2one('product.product', string='Product',  readonly=False,
                                 domain="[('product_tmpl_id','=',product_template_id)]")
    name = fields.Text(string='Description')
    price_unit = fields.Float('Unit Price')
    tax_ids = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])

    def apply_insert(self):
        self.ensure_one()

        if self.order_id.state not in ('draft', 'sent'):
            raise UserError('Unable to insert !!')

        self.order_id.write({
            'order_line': [
                (0, 0, {
                    'product_uom_qty': self.product_uom_qty,
                    'product_id': self.product_id.id,
                    'name': self.name,
                    'price_unit': self.price_unit,
                    'tax_id': self.tax_ids and [(6, 0, self.tax_ids.ids)],
                })]
        })
