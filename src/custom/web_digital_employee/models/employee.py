from odoo import models, fields


class Users(models.Model):
    _inherit = 'hr.employee'

    digital_signature = fields.Binary(string='Signature')
