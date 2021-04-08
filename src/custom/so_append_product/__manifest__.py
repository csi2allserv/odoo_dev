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
{
    'name': 'Add Product to Quotations ',
    'version': '1.0',
    'summary': """Add product to your quotations Easily""",
    'description': """
    This module allows you to add product to your quotations Easily""",
    'category': 'Sales',
    'author': 'Kreative',
    'website': "",
    'license': 'AGPL-3',

    'depends': ['base', 'sale', 'product', 'sales_team'],

    'data': [
        'views/product_product_view.xml',
        'views/product_template_view.xml',
        'wizard/product_product_append_so.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
