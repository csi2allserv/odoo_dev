# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Activity Materials Stock',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['maintenance',
                'stock_account',
                "activiy_materials",
                ],
    'data': [
        'views/maintenance.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': True,
}
