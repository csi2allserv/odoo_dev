#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bulk Expense Report Approval',
    'category': 'Human Resources',
    'sequence': 906,
    'summary': 'Easily approve many employee expenses at once',
    'description': "Odoo app to approve or generate Journal Entries for multiple employee expenses at once via Actions menu.",
    'images': ['static/images/main_thumb.png'],
    'author': 'João Jerónimo',
    
    'version': '1.0',
    'license': 'OPL-1',
    'support': 'joao.jeronimo.pro@gmail.com',
    
    'application': False,
    'installable': True,
    'depends': [
        'hr_expense',
    ],
    'data': [
        'views.xml',
    ],

    #'price': 9,
    #'currency': 'EUR',
}
