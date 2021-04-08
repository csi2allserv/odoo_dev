# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.
{
    'name': "Unique ID for User",
    'summary': """
Auto Generate Unique ID for Users and also Search User By Unique ID
""",
    'description': """
Auto Generate Unique ID for Users and also Search User By Unique ID
User ID
User Unique ID
User Sequence Number
    """,
    "version": "1.0",
    "category": "Extra Tools",
    'author': "Kiran Infosoft",
    "website": "http://www.kiraninfosoft.com",
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'images': ['static/description/demo.gif'],
    "depends": [
        'base',
    ],
    "data": [
        'data/sequence.xml',
        'views/res_users_view.xml',
    ],
    "application": False,
    'installable': True,
}
