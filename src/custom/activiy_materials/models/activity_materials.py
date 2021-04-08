from odoo import tools

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

class mailActivity(models.Model):

    _inherit = 'maintenance.request'

    material_ids = fields.One2many(
        comodel_name='maintenance.task.material', inverse_name='task_id',
        string='Material Used')

class maintenanceTaskMaterial(models.Model):
    """Added Product and Quantity in the Task Material Used."""

    _name = "maintenance.task.material"
    _description = "maintenance Material Used"

    task_id = fields.Many2one(
        comodel_name='maintenance.request', string='Task', ondelete='cascade',
        required=True)
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity')
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Move Analytic Account',
        help='Move created will be assigned to this analytic account',
    )


    @api.multi
    @api.constrains('quantity')
    def _check_quantity(self):
        for material in self:
            if not material.quantity > 0.0:
                raise ValidationError(
                    _('Quantity of material consumed must be greater than 0.')
                )
