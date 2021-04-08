# -*- coding: utf-8 -*-


# Author: Rafael Amaris

{
    'name': 'crm_eco',
    'version': '12.0.1.0.4',
    'category': 'Extra Tools',
    'author': 'Rafael amaris',
    'website': "https://garazd.biz",
    'license': 'LGPL-3',
    'summary': """Print custom product labels with barcode""",
    'images': ['static/description/banner.png'],

    'depends': ['base', 'crm'],
    'data': [
        'views/siplaft_view.xml',
        'views/ficha_prospecto.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}