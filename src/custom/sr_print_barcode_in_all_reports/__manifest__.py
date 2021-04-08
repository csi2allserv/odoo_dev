# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': "Print barcode in sales order, invoice, inventory, and purchase order reports",
    'version': "12.0.0.0",
    'summary': "Print barcode in sales orders, invoices, inventory, and purchase reports",
    'category': 'Extra Tools',
    'description': """
    print barcode in all odoo reports
    barcode in reports
    odoo reports with barcode
    ean13 barcode in odoo reports
    code 128 barcode in odoo reports
    odoo qweb reports with barcode
    barcode in odoo qweb reports
    sales order reports with barcode barcode in sales order pdf report print barcode in sales order qweb report
    purchase order report with barcode barcode in purchase order pdf report print barcode in purchase order qweb report
    request for quotation report with barcode barcode in request for quotation pdf report print in request for quotation qweb report
    customer invoice reports with barcode barcode in customer invoice pdf report print in customer invoice qweb report
    vendor bills reports with barcode barcode in vendor bill pdf report print barcode in vendor bill qweb report
    inventory report with barcode barcode in inventory report pdf report print barode in inventory qweb report
    inherit sales order report template
    inherit customer invoice report template
    inherit vendor bill report template
    inherit inventory report template
    inherit purchase order report template
    inherit request for quotation template
    
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.com",
    'depends': ['base', 'sale_management', 'purchase', 'stock', 'account'],
    'data': [
        'reports/inherited_sale_order_report.xml',
        'reports/inherited_invoice_order_report.xml',
        'reports/inherited_purchase_order_report.xml',
        'reports/inherited_delivery_order_report.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/50QLwLVItSs',
    'images': ['static/description/banner.png'],
    
}
