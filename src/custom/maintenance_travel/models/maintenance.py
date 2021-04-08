

from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    #@api.one
    #@api.depends('viatico_ids')
    #def _prospectus_count(self):
        # _logger.critical('POR EL COUNT2')
        # self.prospectus_count = 1
    #    if self.viatico_ids:
    #        self.Employee_count = len(self.viatico_ids)
    #    else:
    #        self.Employee_count = 0

    viatico_ids = fields.One2many('hr.expense', 'employee_id', string='Dotacion')
    #Employee_count = fields.Integer('Prospectus Count', compute='_prospectus_count')
    sheet_id2 = fields.One2many('hr.expense.sheet', 'maintenance_id', string='Expense Lines', copy=False)

    @api.multi
    def new_transfer_button(self):

        picking_type = self.maintenance_id.sheet_id2

        context = {
            "default_request_id": self.id,
            "default_equipment_id": self.equipment_id.id,
            "default_origin": self.name,
        }
    
    


