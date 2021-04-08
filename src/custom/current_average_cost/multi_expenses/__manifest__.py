# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'multi expenses',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': [
                'hr_expense',
                ],
    'data': [
        'views/expense_multi.xml',
    ],
    'installable': True,
    'application': True,
}
