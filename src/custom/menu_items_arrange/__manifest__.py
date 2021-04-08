# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.

{
    'name': "App Menu Items Arrange (A-Z,New-Old,Asen-Desc)",

    'summary': """
        This module allows menu items of Odoo App menu to be arranged Alphabetically or According to installed date.""",

    'description': """
        Odoo Menu apps can be arranged in both ascending and descending order based alphabetically/Installed date or Sequencially.
    """,

    'author': "10 Orbits",
    'website': 'https://erp.10orbits.com',
    'category': 'Tools',
    'company': '10 Orbits',
    'version': '0.1',
    'images': ['static/description/banner.png'],
    # any module necessary for this one to work correctly
    'depends': ['base','base_setup'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/css.xml'
    ],
    'installable': True,
    # 'price': 50,
    # 'currency': 'USD',
    'license': 'AGPL-3',

}
