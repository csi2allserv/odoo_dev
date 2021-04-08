from odoo import tools

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class teamCategory(models.Model):

    _name = "team.category"
    _description = "Sistemas Category"

    name = fields.Char(string="Equipo", required=True)
    color = fields.Integer(string='Color Index')
    category_ids = fields.Many2many('technical.maintenance', 'employee_category_rel', 'category_id', 'emp_id')
    category2_ids = fields.Many2many('technical.maintenance', 'employees_category_rel', 'category2_id', 'emp2_id')
    sistema_id = fields.Many2one('tipo.sistemas')
    sistema2_id = fields.Many2one('tipo.sistemas')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "System name already exists !"),
    ]

class MaintenanceServicesStage(models.Model):
    """ Model for case stages. This models the main stages of a Maintenance Request management flow. """

    _name = 'services.stage'
    _description = 'services Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Plegado en el flojo de servicio')
    done = fields.Boolean('Servicio hecho')

class technicalMaintenance(models.Model):

    _name = 'technical.maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "priority desc, date asc, id desc" 
    

    @api.returns('self')
    def _default_stage(self):
        return self.env['services.stage'].search([], limit=1)


    stage_id = fields.Many2one('services.stage', string='Stage', ondelete='restrict', track_visibility='onchange',
                               group_expand='_read_group_stage_ids', default=_default_stage, copy=False)
    archive = fields.Boolean(default=False,
                             help="Set archive to true to hide the maintenance request without deleting it.")
    kanban_state = fields.Selection(
        [('normal', 'Asignado'), ('blocked', 'Blocked')],
        string='Kanban State', required=True, default='normal', track_visibility='onchange')
    #user_id = fields.Many2one('res.users', string='Technician', track_visibility='onchange',
    #                          oldname='technician_user_id')
    disponibilidad = fields.Selection(
       [('si', 'Si'),('no', 'No')],
        string='Disponibilidad?')
    tipo_mantenimiento_id = fields.Many2one('tipos.mantenimiento',  string='Tipo de mantenimiento')
    sistema_id = fields.Many2one('tipo.sistemas',  string='Tipo de sistema')
    sistema2_id = fields.Many2one('tipo.sistemas', string='Tipo de sistema')
    motivo = fields.Selection(
        [('funcionario', 'Funcionario no puede antender'), ('funcionario1', 'Funcionario no se encuentra')]
    )
    category_ids = fields.Many2many(
        'team.category', 'employee_category_rel',
        'emp_id', 'category_id',
        string='Trabajo en?')
    category2_ids = fields.Many2many(
        'team.category', 'employees_category_rel',
        'emp2_id', 'category2_id',
        string='Trabajo en?')

    otroSistema2 = fields.Selection(
       [('si', 'Si'),('no', 'No')],
        string='Otro sistema?', default='no'
    )

    maintenance_request_id = fields.Many2one('maintenance.request',
                                 'Purchase Request',
                                 ondelete='cascade', readonly=True)

    priority = fields.Selection([('0', 'Very Low'), ('1', 'Importante'), ('2', 'Urgencia'), ('3', 'Emergencia')], string='Priority')
    date = fields.Date('fecha')
    origin = fields.Char(
        'Source Document', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Reference of the document")
    city_id = fields.Many2one('res.city', string='Ciudad', readonly=True)
    color = fields.Integer('Color Index')
    name = fields.Char('Numero de servicio', readonly=True)
    partner_id = fields.Char('Entidad', readonly=True)
    city_id_service = fields.Char('Ciudad')
    location_id = fields.Many2one('crm.customer.location', \
                                  string='Codigo', readonly=True)
    schedule_date = fields.Date('Fecha de programación', readonly=True)
    description = fields.Text('Falla reportada', readonly=True)
    code = fields.Char(string='Codigo', readonly=True)
    user_id = fields.Many2one(
        'res.users', 'Asignado a:',
        default=lambda self: self.env.user,
        index=True)



    @api.multi
    def action_openRequestLineTreeView(self):
        """
        :return dict: dictionary value for created view
        """
        request_maintenance_line_ids = []
        for line in self:
            request_maintenance_line_ids += line.maintenance.ids

        domain = [('id', 'in', request_maintenance_line_ids)]

        return {'name': _('Maintenance Request Lines'),
                'type': 'ir.actions.act_window',
                'res_model': 'maintenance.request',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': domain}

    @api.multi
    def archive_equipment_request(self):
        self.write({'archive': True})

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    #Filtro de id para tipo de sitema 1
    @api.multi
    @api.onchange('sistema_id', 'tipo_mantenimiento_id')
    def location_id_change(self):
        if not self.sistema_id and not self.tipo_mantenimiento_id:
            return

        domain = []
        if self.tipo_mantenimiento_id:
            domain.append(('tipo_mantenimiento_id', '=', self.tipo_mantenimiento_id.id))
        if self.sistema_id:
            domain.append(('sistema_id', '=', self.sistema_id.id))
        if len(domain) > 1:
                domain = ['&'] + domain
        locations = self.env['tipo.sistemas']. \
            search(domain, limit=100)
        ids = [location.id for location in locations]
        return {'domain': {
            'sistema_id': [('id', 'in', ids)]}
        }

    # Filtro de id para tipo de sitema 2
    @api.multi
    @api.onchange('sistema2_id', 'tipo_mantenimiento_id')
    def location_id_change2(self):
        if not self.sistema2_id and not self.tipo_mantenimiento_id:
            return

        domain = []
        if self.tipo_mantenimiento_id:
            domain.append(('tipo_mantenimiento_id', '=', self.tipo_mantenimiento_id.id))
        if self.sistema2_id:
            domain.append(('sistema2_id', '=', self.sistema2_id.id))
        if len(domain) > 1:
                domain = ['&'] + domain
        locations = self.env['tipo.sistemas']. \
            search(domain, limit=100)
        ids = [location.id for location in locations]
        return {'domain': {
            'sistema2_id': [('id', 'in', ids)]}
        }

    #Filtro para categoria 1
    @api.multi
    @api.onchange('category_ids', 'sistema_id')
    def location_id_sistem(self):
        if not self.category_ids and not self.sistema_id:
            return

        domain = []
        if self.sistema_id:
            domain.append(('sistema_id', '=', self.sistema_id.id))
        if self.sistema2_id:
            domain.append(('sistema2_id', '=', self.sistema2_id.id))
        if len(domain) > 1:
                domain = ['&'] + domain
        locations = self.env['team.category']. \
            search(domain, limit=100)
        ids = [location.id for location in locations]
        return {'domain': {
            'category_ids': [('id', 'in', ids)]}
        }

    # Filtro para categoria 2



    class tiposDeMantenimiento(models.Model):

        _name = 'tipos.mantenimiento'

        name = fields.Char('Tipo de mantenimiento')

    class tiposDeSistema(models.Model):
        _name = 'tipo.sistemas'

        name= fields.Char()
        sistema_id = fields.Char('Tipo de Sistema')
        sistema2_id = fields.Char('Tipo de Sistema')
        tipo_mantenimiento_id = fields.Many2one('tipos.mantenimiento', string='Tipo de mantenimiento', required='True')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            if operator in positive_operators:
                locations = self.search([
                    '|',
                    ('name', operator, name)
                ])
        else:
            locations = self.search(args, limit=limit)
        return locations.name_get()


