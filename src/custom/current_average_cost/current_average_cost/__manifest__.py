# -*- encoding: utf-8 -*-
{
    'name' : 'SW - Current Average Cost',
    'version' : '12.0.1.0',
    'category'  : 'Warehouse',
    'summary': """Displays product average cost for current stock.""",
    'author' : 'Smart Way Business Solutions',
    'website' : 'https://www.smartway.co',
    'license':  "Other proprietary",
    'depends' : ['product','stock','stock_account'],
    'data' : [
            'view/product.xml'
                ],
    "images":  ['static/description/image.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
