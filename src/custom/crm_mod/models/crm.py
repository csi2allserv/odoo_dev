# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    John W. Viloria Amaris <john.viloria.amaris@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    #REQ #20
    @api.model
    def create(self, vals):
        lead_type = dict(self._fields['tipo_opor'].selection).\
            get(vals.get('tipo_opor'))
        if vals.get('categs_ids', False):
            categs_ids = vals.get('categs_ids', False)
            try:
                ids = categs_ids[0][2]
                cat_names = [cat.name for cat in \
                    self.env['product.category'].\
                    search([('id','in',ids)])]
            except Exception as e:
                _logger.critical('Error: %e'%e)
                cat_names = []
            vals['name'] = '{0} {1}'.format(lead_type, ', '.join(cat_names))
        else:
            cat_names = []
        return super(CrmLead, self).create(vals)