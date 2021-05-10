# -*- coding: utf-8 -*-
{
    'name': "crm_mod",
    'description':'''\
CRM Mod
==================================

Modificaciones varias al módulo de crm.
    ''',
    'summary': """ Modificaciones al modulo CRM""",
    'author': "ITSoluciones S.A.S ",
    'website': "http://itsoluciones.net/",
    'category': 'Allservice',
    'version': '0.1',
    'depends': [
        'sale', 'product_brand',
        'product',                      #REQ #18
        ],
    'data': [
        'views/crm_mod.xml',
        'views/pricelist_view.xml',     #REQ #18
        ],

    'installable': True,
    'auto_install': False,
}