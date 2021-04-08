# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'travel maintenance',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['maintenance',
                'hr_expense',
                ],
    'data': [
        'views/maintenance.xml',
    ],
    'installable': True,
    'application': True,
}
