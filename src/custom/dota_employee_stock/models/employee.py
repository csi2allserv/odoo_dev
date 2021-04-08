

from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models

class siplaft(models.Model):
    _inherit = 'hr.employee'

    @api.one
    @api.depends('dotacion_ids')
    def _prospectus_count(self):
        # _logger.critical('POR EL COUNT2')
        # self.prospectus_count = 1
        if self.dotacion_ids:
            self.Employee_count = len(self.dotacion_ids)
        else:
            self.Employee_count = 0
            

    dotacion_ids = fields.One2many('stock.picking', 'employee_id', string='Dotacion')
    Employee_count = fields.Integer('Prospectus Count', compute='_prospectus_count')
    suma = fields.Many2one('product.template', 'standard_price')