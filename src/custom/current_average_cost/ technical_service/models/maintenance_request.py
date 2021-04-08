from odoo import tools

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    line_ids = fields.One2many('technical.maintenance', 'maintenance_request_id',
                               'maintenance',
                               readonly=False,
                               copy=True,
                               track_visibility='onchange')
    line_count = fields.Integer(
        string='Purchase Request Line count',
        compute='_compute_line_count',
        readonly=True
    )

    @api.depends('line_ids')
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.mapped('line_ids'))

    #@api.multi
    #def action_view_maintenance_request_line(self):
    #    action = self.env.ref(
    #        'technical_service.purchase_request_line_form_action').read()[0]
    #    lines = self.mapped('line_ids')
    #    if len(lines) > 1:
    #        action['domain'] = [('id', 'in', lines.ids)]
    #    elif lines:
    #        action['views'] = [(self.env.ref(
    #            'technical_service.technical_request_form_view').id, 'form')]
    #        action['res_id'] = lines.ids[0]
    #    return action
