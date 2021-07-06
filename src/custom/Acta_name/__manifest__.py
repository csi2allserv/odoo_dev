{
    'name': "Acta",
    'summary': "Acta para mantenimientos",
    'description': """Long description""",
    'author': "Efrain Rojas, William Acosta ",
    'website': "http://www.example.com",
    'category': "Mantenimiento",
    'version': '12.0.1',
    'depends': ['base'],
    'data': [
        'views/acta_servicio.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'report/pdfacta.xml',
        'report/presentacionpdfacta.xml',
    ],
    #'demo': ['demo.xml'],
}

