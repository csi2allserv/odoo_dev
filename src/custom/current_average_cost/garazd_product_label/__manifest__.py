# -*- coding: utf-8 -*-

# Copyright (C) 2019-2020 Garazd Creation (<https://garazd.biz/>)
# Author: Yurii Razumovskyi (<support@garazd.biz>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Custom Product Labels',
    'version': '12.0.1.0.4',
    'category': 'Extra Tools',
    'author': 'Garazd Creation',
    'website': "https://garazd.biz",
    'license': 'LGPL-3',
    'summary': """Print custom product labels with barcode""",
    'images': ['static/description/banner.png'],
    'description': """
Module allows to print custom product barcode labels and tags on different paper formats.
This module include the one label template with size: 57x35mm, paperformat: A4 (21 pcs per sheet, 3 pcs x 7 rows).
It is possible to add additional label templates with our other modules.
    """,
    'depends': ['product', 'backend_multi_barcode'],
    'data': [
        'wizard/print_product_label_views.xml',
        'report/product_label_templates.xml',
        'report/product_label_reports.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
