# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Dota Employee stock',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['hr',
                'stock',
                ],
    'data': [
        'views/employee.xml',
    ],
    'installable': True,
    'application': True,
}
