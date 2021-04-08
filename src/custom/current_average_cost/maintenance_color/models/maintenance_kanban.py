
import logging

from odoo import tools

from odoo import models, fields, api
from odoo.tools.translate import _

import datetime
import pytz

_logger = logging.getLogger(__name__)

def get_server_time(tz_server=None):

        now_utc = datetime.datetime.utcnow() #Our UTC naive time from server,

        #_logger.warning("now_utc: %s", now_utc)

        if tz_server:

            local_tz = pytz.timezone(tz_server) #Our Local timezone
            #_logger.warning("local_tz: %s, Offset: %s", local_tz, tz_offset)

            now_utc = pytz.utc.localize(now_utc) #Add Timezone information
            #_logger.warning("new_tz: %s", now_utc)

            server_time = now_utc.astimezone(local_tz) # Convert to local
            #_logger.warning("server_time: %s", server_time)

            result = server_time
        else:
            now_utc = datetime.date.today()
            result = now_utc

        return result

class ProjectKanban(models.Model):

    _inherit = 'maintenance.request'


    def get_color_date_of_assignment(self, date_of_assignment):

        dout = fields.Date.from_string(date_of_assignment)
        dnow = get_server_time()

        if (dnow - dout).days > 0:
            return 1
        else:
            return 0

    @api.onchange('date_of_assignment')
    def _onchange_deadline(self):

        date_of_assignment = self.date_of_assignment
        if date_of_assignment:
            self.color = self.get_color_date_of_assignment(date_of_assignment)

    @api.model
    def _check_deadline(self):

        maintenance_request_obj = self.env['maintenance.request']
        maintenance_request_search = maintenance_request_obj.sudo().search([('kanban_state', '!=', 'done')])

        for task in maintenance_request_search:
            date_of_assignment = task.date_of_assignment
            if date_of_assignment:
                color = self.get_color_date_of_assignment(date_of_assignment)
                task.write({'color': color})


