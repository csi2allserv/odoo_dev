# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'expenses all',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['hr_expense',
                'base',
                'maintenance',
                'stock',
                ],
    'data': [
        'views/expense_all.xml',
        'data/expense_sequence.xml',
    ],
    'installable': True,
    'application': True,
}