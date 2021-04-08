# -*- coding: utf-8 -*-
{
    'name': "odoo_mo_monthlypurchases",

    'summary': """
     MPR  Get Report Contains All Purchased Product by Month in xls , Pdf , You can also Preview before  Printing""",

    'description': """
        Print Report Contain Purchased Product By Month,Range Date in xls ,Pdf,Life Preview
    """,

    'author': " ODOO MO ",
    'website': "https://www.facebook.com/groups/246493319957599/",


    'category': 'Purchase',
    'version': '12.0',
    "license": "AGPL-3",
'images': ['static/description/3.png'],


    # any module necessary for this one to work correctly
    'depends': ['base','purchase','report_xlsx'],

    # always loaded
    'data': [
        'wizards/wizard_view.xml',
        'reports/template.xml',
        'reports/report.xml',
    ],
'qweb': [
        'static/src/xml/report_tmpl.xml'],

}
