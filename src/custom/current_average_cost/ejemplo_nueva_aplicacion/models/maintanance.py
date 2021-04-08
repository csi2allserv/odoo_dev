from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ejemplo_nueva_clase(models.Model):
    _inherit = 'maintenance.request'

    campo_ejemplo = fields.Char('campo nuevo')
    campoejemplo2 = fields.Text('campo de texto')
