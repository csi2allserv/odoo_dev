# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Activity materials',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['maintenance',
                'product',
                "stock_account",
                ],
    'data': [
        'views/activity_materials.xml'
    ],
    'installable': True,
    'application': True,
}
