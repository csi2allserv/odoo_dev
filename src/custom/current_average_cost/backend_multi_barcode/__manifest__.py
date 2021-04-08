# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################
{
    'name': 'Backend Multi Barcode',
    'version': '12.1.20200329',
    'summary': 'Multi barcode allow you set multi barcode/reference from many vendor on one product. Make it available search on Sale/Purchase/Inventory..',
    'sequence': 0,
    'description': """
    Multi barcode product at backend
    """,
    'live_test_url': 'https://demo13.domiup.com',
    'category': 'Inventory',
    'depends': [
        'product',
        'stock',
        'sale',
        'barcodes',
        'purchase'
    ],
    'data': [
        'views/product_multi_barcode_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        # asset

        # security
        'security/ir.model.access.csv'
    ],
    'price': 0,
    'currency': 'EUR',
    'license': 'OPL-1',
    'author': "Domiup",
    'support': 'domiup.contact@gmail.com',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False
}