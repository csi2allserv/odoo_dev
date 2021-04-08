# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.
{
    'name': "Unique ID for purcharse",
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
    'author': "Rafael Amaris",
    'price': 0.0,
    'currency': 'EUR',
    "depends": [
        'purchase_request',
    ],
    "data": [
        'data/sequence.xml',
        'views/res_purchase_view.xml',
        'views/purchase_request_line.xml',
    ],
    "application": False,
    'installable': True,
}
