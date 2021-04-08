{
    'name': 'Rapport de paie en excel',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'payroll',
    'sequence': 60,
    'summary': 'Générer le rapport au format xlsx',
    'description': "It shows payroll report in excel for given month",
    'author':'Roots-Technologies',
    'depends': ['base','hr', 'hr_payroll'],
    'data': ['wizard/payroll_report_wiz.xml'
      ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
