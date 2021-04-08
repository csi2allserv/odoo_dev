# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name' : 'Expense Excel Report',
    'version': '12.0',
    'author': 'Rafael Amaris',
    'category': 'Purchase',
    'license': 'LGPL-3',
    'summary': 'Excel sheet for Purchase Order',
    'description': """ Purchase order excel report
When user need to print the excel report in purchase order select the purchase order list and
user need to click the "Purchase order Excel Report" button and message will appear.select the "Print Excel report"button
for generating the purchase order excel file""",
    'depends': [
        'hr_expense','base',
    ],
    'data': [
        'wizard/expense_xls_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
