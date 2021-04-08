from . import maintenance

from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'maintenance.stage'

    send_services = fields.Boolean(
        help="If you mark this check, when a task goes to this state, "
             "it will consume the associated materials",
    )


