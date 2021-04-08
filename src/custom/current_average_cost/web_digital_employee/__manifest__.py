# See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Digital Employee',
    'version': '12.0.1.0.0',
    'author': 'Rafael Amaris Martinez',
    'depends': ['web',
                'hr'
                ],
    "license": "AGPL-3",
    'category': 'Tools',
    'description': '''
     This module provides the functionality to store digital signature
     Example can be seen into the User's form view where we have
        added a test field under signature.
    ''',
    'summary': '''
        Touch screen enable so user can add signature with touch devices.
        Digital signature can be very usefull for documents.
    ''',
    'data': [
        'views/web_digita_sign_view.xml',
        'views/employee_view.xml'],
    'installable': True,
    'auto_install': False,
}
