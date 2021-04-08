from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ventana(models.Model):

    _name = 'prueba'
    
    name = fields.Char('nombre')
    categ_id = fields.Char('Id') 