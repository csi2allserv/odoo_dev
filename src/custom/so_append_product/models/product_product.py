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
from odoo import models, api, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def open_so_product_append(self):

        context = {
            'default_product_template_id': self.product_tmpl_id.id,
            'default_product_id': self.id,
            'default_name': self.display_name,
            'default_price_unit': self.list_price,
        }
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'product.product.append.so',
                'target': 'new',
                'context': context,
                }


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def open_so_product_template_append(self):

        product_id = False
        if len(self.product_variant_ids) == 1:
            product_id = self.product_variant_ids[0].id

        context = {
            'default_product_template_id': self.id,
            'default_product_id': product_id,
            'default_name': self.display_name,
            'default_price_unit': self.list_price,
        }

        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'product.product.append.so',
                'target': 'new',
                'context': context,
                }


