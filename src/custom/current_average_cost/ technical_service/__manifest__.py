# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'technical service',
    'version': '1.12',
    'author': 'Rafael Amaris',
    'sequence': 0,
    'depends': ['maintenance',
                ],
    'data': [
        'views/maintenance_views.xml',
        'views/type_maintenance.xml',
        'views/type_system.xml',
        'views/maintenance_request.xml',
        'data/services_data.xml',
        'wizard/purchase_request_line_make_purchase_order_view.xml'
    ],
    'installable': True,
    'application': True,
}
