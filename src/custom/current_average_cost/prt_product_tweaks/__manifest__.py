# -*- coding: utf-8 -*-
{
    'name': 'Product Tweaks. Multiple Internal Reference Product Code SKU',
    'version': '12.0.1.0',
    'author': 'Ivan Sokolov, Cetmix',
    'category': 'Sales',
    'license': 'LGPL-3',
    'website': 'https://cetmix.com',
    'live_test_url': 'https://demo.cetmix.com',
    'summary': """Multiple internal references for products """,
    'description': """
    Multiple Internal References SKU Product Codes
""",
    'depends': ['product', 'stock'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/prt_product.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
