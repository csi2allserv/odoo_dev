# -*- coding: utf-8 -*-
{
    'name': "Pruebas",

    'summary': """
        aplicacion de prueba """,

    'description': """
        Lorem ipsum dolor sit amet,
         consectetur adipiscing elit. 
         Maecenas in libero pharetra, 
         maximus urna non, rhoncus sapien.
          Etiam sodales et turpis at suscipit.
           Mauris sit amet porttitor metus. 
           Curabitur dapibus ultricies velit non congue. 
           Nam nulla orci, vehicula quis luctus quis,
            molestie in enim. Aenean ac maximus leo. Nulla facilisi.
             Aenean metus ante, eleifend id blandit non, porta ut magna.
              Mauris dui risus, dapibus ut condimentum et, 
              posuere vel risus. Ut a magna arcu. Pellentesque 
              euismod auctor quam, et euismod elit efficitur eget
              . Nunc vestibulum urna vel ante sodales convallis. 
              Ut luctus auctor lorem
    """,

    'author': "William Acosta",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,
}