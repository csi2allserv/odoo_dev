# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'expense maintenance',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['maintenance',
                "hr_expense",
                ],
    'data': [
        'views/expense_maintenance.xml'
    ],
    'installable': True,
    'application': True,
}
