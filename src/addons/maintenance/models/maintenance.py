# -*- coding: utf-8 -*-
import time
from calendar import calendar
from calendar import day_name
from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from datetime import timedelta



class MaintenanceStage(models.Model):
    """ Model for case stages. This models the main stages of a Maintenance Request management flow. """

    _name = 'maintenance.stage'
    _description = 'Maintenance Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Maintenance Pipe')
    done = fields.Boolean('Request Done')


class MaintenanceEquipmentCategory(models.Model):
    _name = 'maintenance.equipment.category'
    _inherit = ['mail.alias.mixin', 'mail.thread']
    _description = 'Maintenance Equipment Category'

    @api.one
    @api.depends('equipment_ids')
    def _compute_fold(self):
        self.fold = False if self.equipment_count else True

    name = fields.Char('Category Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    technician_user_id = fields.Many2one('res.users', 'Responsible', track_visibility='onchange', default=lambda self: self.env.uid, oldname='user_id')
    color = fields.Integer('Color Index')
    note = fields.Text('Comments', translate=True)
    equipment_ids = fields.One2many('maintenance.equipment', 'category_id', string='Equipments', copy=False)
    equipment_count = fields.Integer(string="Equipment", compute='_compute_equipment_count')
    maintenance_ids = fields.One2many('maintenance.request', 'category_id', copy=False)
    maintenance_count = fields.Integer(string="Maintenance Count", compute='_compute_maintenance_count')
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete='restrict', required=True,
        help="Email alias for this equipment category. New emails will automatically "
        "create a new equipment under this category.")
    fold = fields.Boolean(string='Folded in Maintenance Pipe', compute='_compute_fold', store=True)

    @api.multi
    def _compute_equipment_count(self):
        equipment_data = self.env['maintenance.equipment'].read_group([('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in equipment_data])
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    @api.multi
    def _compute_maintenance_count(self):
        maintenance_data = self.env['maintenance.request'].read_group([('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in maintenance_data])
        for category in self:
            category.maintenance_count = mapped_data.get(category.id, 0)

    @api.model
    def create(self, vals):
        self = self.with_context(alias_model_name='maintenance.request', alias_parent_model_name=self._name)
        if not vals.get('alias_name'):
            vals['alias_name'] = vals.get('name')
        category_id = super(MaintenanceEquipmentCategory, self).create(vals)
        category_id.alias_id.write({'alias_parent_thread_id': category_id.id, 'alias_defaults': {'category_id': category_id.id}})
        return category_id

    @api.multi
    def unlink(self):
        MailAlias = self.env['mail.alias']
        for category in self:
            if category.equipment_ids or category.maintenance_ids:
                raise UserError(_("You cannot delete an equipment category containing equipments or maintenance requests."))
            MailAlias += category.alias_id
        res = super(MaintenanceEquipmentCategory, self).unlink()
        MailAlias.unlink()
        return res

    def get_alias_model_name(self, vals):
        return vals.get('alias_model', 'maintenance.equipment')

    def get_alias_values(self):
        values = super(MaintenanceEquipmentCategory, self).get_alias_values()
        values['alias_defaults'] = {'category_id': self.id}
        return values


class MaintenanceEquipment(models.Model):
    _name = 'maintenance.equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Equipment'

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'owner_user_id' in init_values and self.owner_user_id:
            return 'maintenance.mt_mat_assign'
        return super(MaintenanceEquipment, self)._track_subtype(init_values)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name and record.serial_no:
                result.append((record.id, record.name + '/' + record.serial_no))
            if record.name and not record.serial_no:
                result.append((record.id, record.name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        equipment_ids = []
        if name:
            equipment_ids = self._search([('name', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
        if not equipment_ids:
            equipment_ids = self._search([('name', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(equipment_ids).name_get()

    name = fields.Char('Equipment Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    technician_user_id = fields.Many2one('res.users', string='Technician', track_visibility='onchange', oldname='user_id')
    owner_user_id = fields.Many2one('res.users', string='Owner', track_visibility='onchange')
    category_id = fields.Many2one('maintenance.equipment.category', string='Equipment Category',
                                  track_visibility='onchange', group_expand='_read_group_category_ids')
    partner_id = fields.Many2one('res.partner', string='Vendor', domain="[('supplier', '=', 1)]")
    partner_ref = fields.Char('Vendor Reference')
    location = fields.Char('Location')
    model = fields.Char('Model')
    serial_no = fields.Char('Serial Number', copy=False)
    assign_date = fields.Date('Assigned Date', track_visibility='onchange')
    effective_date = fields.Date('Effective Date', default=fields.Date.context_today, required=True, help="Date at which the equipment became effective. This date will be used to compute the Mean Time Between Failure.")
    cost = fields.Float('Cost')
    note = fields.Text('Note')
    warranty_date = fields.Date('Warranty Expiration Date', oldname='warranty')
    color = fields.Integer('Color Index')
    scrap_date = fields.Date('Scrap Date')
    maintenance_ids = fields.One2many('maintenance.request', 'equipment_id')
    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string="Maintenance Count", store=True)
    maintenance_open_count = fields.Integer(compute='_compute_maintenance_count', string="Current Maintenance", store=True)
    period = fields.Integer('Days between each preventive maintenance')
    next_action_date = fields.Date(compute='_compute_next_maintenance', string='Date of the next preventive maintenance', store=True)
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
    maintenance_duration = fields.Float(help="Maintenance Duration in hours.")

    @api.depends('effective_date', 'period', 'maintenance_ids.request_date', 'maintenance_ids.close_date')
    def _compute_next_maintenance(self):
        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period > 0):
            next_maintenance_todo = self.env['maintenance.request'].search([
                ('equipment_id', '=', equipment.id),
                ('maintenance_type', '=', 'preventive'),
                ('stage_id.done', '!=', True),
                ('close_date', '=', False)], order="request_date asc", limit=1)
            last_maintenance_done = self.env['maintenance.request'].search([
                ('equipment_id', '=', equipment.id),
                ('maintenance_type', '=', 'preventive'),
                ('stage_id.done', '=', True),
                ('close_date', '!=', False)], order="close_date desc", limit=1)
            if next_maintenance_todo and last_maintenance_done:
                next_date = next_maintenance_todo.request_date
                date_gap = next_maintenance_todo.request_date - last_maintenance_done.close_date
                # If the gap between the last_maintenance_done and the next_maintenance_todo one is bigger than 2 times the period and next request is in the future
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2 and next_maintenance_todo.request_date > date_now:
                    # If the new date still in the past, we set it for today
                    if last_maintenance_done.close_date + timedelta(days=equipment.period) < date_now:
                        next_date = date_now
                    else:
                        next_date = last_maintenance_done.close_date + timedelta(days=equipment.period)
            elif next_maintenance_todo:
                next_date = next_maintenance_todo.request_date
                date_gap = next_maintenance_todo.request_date - date_now
                # If next maintenance to do is in the future, and in more than 2 times the period, we insert an new request
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2:
                    next_date = date_now + timedelta(days=equipment.period)
            elif last_maintenance_done:
                next_date = last_maintenance_done.close_date + timedelta(days=equipment.period)
                # If when we add the period to the last maintenance done and we still in past, we plan it for today
                if next_date < date_now:
                    next_date = date_now
            else:
                next_date = self.effective_date + timedelta(days=equipment.period)
            equipment.next_action_date = next_date

    @api.one
    @api.depends('maintenance_ids.stage_id.done')
    def _compute_maintenance_count(self):
        self.maintenance_count = len(self.maintenance_ids)
        self.maintenance_open_count = len(self.maintenance_ids.filtered(lambda x: not x.stage_id.done))

    @api.onchange('category_id')
    def _onchange_category_id(self):
        self.technician_user_id = self.category_id.technician_user_id

    _sql_constraints = [
        ('serial_no', 'unique(serial_no)', "Another asset already exists with this serial number!"),
    ]

    @api.model
    def create(self, vals):
        equipment = super(MaintenanceEquipment, self).create(vals)
        if equipment.owner_user_id:
            equipment.message_subscribe(partner_ids=[equipment.owner_user_id.partner_id.id])
        return equipment

    @api.multi
    def write(self, vals):
        if vals.get('owner_user_id'):
            self.message_subscribe(partner_ids=self.env['res.users'].browse(vals['owner_user_id']).partner_id.ids)
        return super(MaintenanceEquipment, self).write(vals)

    @api.model
    def _read_group_category_ids(self, categories, domain, order):
        """ Read group customization in order to display all the categories in
            the kanban view, even if they are empty.
        """
        category_ids = categories._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    def _create_new_request(self, date):
        self.ensure_one()
        self.env['maintenance.request'].create({
            'name': _('Preventive Maintenance - %s') % self.name,
            'request_date': date,
            'schedule_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'maintenance_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'user_id': self.technician_user_id.id,
            'maintenance_team_id': self.maintenance_team_id.id,
            'duration': self.maintenance_duration,
            })

    @api.model
    def _cron_generate_requests(self):
        """
            Generates maintenance request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period', '>', 0)]):
            next_requests = self.env['maintenance.request'].search([('stage_id.done', '=', False),
                                                    ('equipment_id', '=', equipment.id),
                                                    ('maintenance_type', '=', 'preventive'),
                                                    ('request_date', '=', equipment.next_action_date)])
            if not next_requests:
                equipment._create_new_request(equipment.next_action_date)

#funcion creada por william acosta y efrain rojas
#tener presente que una vez se cambie el año toca cambiar los dias festivos
def day_habil():
    dia = date.today()
    cont = 1
    for x in range(4):
        cont = cont + 1
        tomorrow = dia + timedelta(cont)
        wek = day_name[tomorrow.weekday()]
        d1 = tomorrow.strftime("%d/%m")
        print(str(wek))
        if wek == "sábado":
            cont = cont + 1
            print(str(wek))
        elif wek == "domingo":
            cont = cont + 1
            print(str(wek))
        elif d1 == "01/01":
            cont = cont + 1
        elif d1 == "11/01":
            cont = cont + 1
        elif d1 == "22/03":
            cont = cont + 1
        elif d1 == "01/04":
            cont = cont + 1
        elif d1 == "02/04":
            cont = cont + 1
        elif d1 == "01/05":
            cont = cont + 1
        elif d1 == "17/05":
            cont = cont + 1
        elif d1 == "07/06":
            cont = cont + 1
        elif d1 == "14/06":
            cont = cont + 1
        elif d1 == "05/07":
            cont = cont + 1
        elif d1 == "20/07":
            cont = cont + 1
        elif d1 == "07/08":
            cont = cont + 1
        elif d1 == "16/08":
            cont = cont + 1
        elif d1 == "18/10":
            cont = cont + 1
        elif d1 == "01/11":
            cont = cont + 1
        elif d1 == "15/11":
            cont = cont + 1
        elif d1 == "08/12":
            cont = cont + 1
        elif d1 == "25/12":
            cont = cont + 1
    return tomorrow


def create_excel(codigo):
    print(str(codigo))
    pass


class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Request'
    _order = "id desc"

    @api.model
    def _default_location_type(self):
        return self.env['crm.customer.location.type'].search([('name', '=', 'Oficina')],limit=1)

    @api.returns('self')
    def _default_stage(self):
        return self.env['maintenance.stage'].search([], limit=1)

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'stage_id' in init_values and self.stage_id.sequence <= 1:
            return 'maintenance.mt_req_created'
        elif 'stage_id' in init_values and self.stage_id.sequence > 1:
            return 'maintenance.mt_req_status'
        return super(MaintenanceRequest, self)._track_subtype(init_values)

    def _get_default_team_id(self):
        MT = self.env['maintenance.team']
        team = MT.search([('company_id', '=', self.env.user.company_id.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id


    name = fields.Char('Subjects', maintenance_type={'corrective': [('required', True)], 'proyecto': [('readonly', True)]})
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    description = fields.Text('Description')
    request_date = fields.Date('Request Date', help="Fecha de inicio sodexo")
    end_date = fields.Date('Fecha fin', track_visibility='onchange',
                               help="Fecha fin sodexo")
    date_of_assignment = fields.Datetime('Fecha de Asignacion', track_visibility='onchange',  help="Fecha fin sodexo" , default=lambda self: fields.Datetime.now())
    owner_user_id = fields.Many2one('res.users', string='Created by User', default=lambda s: s.env.uid)
    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id', string='Category', store=True, readonly=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Tipo de Sistema',
                                   ondelete='restrict', index=True)
    user_id = fields.Many2one('res.users', string='Technician', track_visibility='onchange', oldname='technician_user_id')
    stage_id = fields.Many2one('maintenance.stage', string='Stage', ondelete='restrict', track_visibility='onchange',
                               group_expand='_read_group_stage_ids', default=_default_stage, copy=False)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Importante'), ('2', 'Urgencia'), ('3', 'Emergencia')], string='Priority')
    color = fields.Integer('Color Index')
    close_date = fields.Date('Close Date', help="Date the maintenance was finished. ")
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal', track_visibility='onchange')
    # active = fields.Boolean(default=True, help="Set active to false to hide the maintenance request without deleting it.")
    archive = fields.Boolean(default=False, help="Set archive to true to hide the maintenance request without deleting it.")
    maintenance_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive'),('proyecto', 'P.especial')], string='Maintenance Type', default="corrective")
    schedule_date = fields.Date('Scheduled Date', help="Date the maintenance team plans the maintenance.  It should not differ much from the Request Date. " , default=lambda self: day_habil())
    maintenance_team_id = fields.Many2one('maintenance.team', string='Proceso', required=False, default=_get_default_team_id)
    duration = fields.Float(help="Duration in hours and minutes.", default='8')
    location_type_id = fields.Many2one('crm.customer.location.type', default=_default_location_type, \
                                       string='Tipo de Ubicacion')
    city_id = fields.Many2one('res.city', string='Ciudad', readonly=True)
    codigos = fields.Char(string="codigos")
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', track_sequence=1, index=True,
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    #codigo realizado por william acosta
    planificador = fields.Selection([('p1', 'personal 1'), ('p2', 'personal 2'), ('p3', 'personal 3'), ('p4', 'personal 4'), ('p5', 'personal 5')],)
    location = fields.Char()
    validador = fields.Boolean(default=False)
    tecnicoApoyo1 = fields.Many2one('res.users', string='Tecnico de apoyo')
    tecnicoApoyo2 = fields.Many2one('res.users', string='Tecnico de apoyo')
    tecnicoApoyo3 = fields.Many2one('res.users', string='Tecnico de apoyo')
    tecnicoApoyo4 = fields.Many2one('res.users', string='Tecnico de apoyo')
    tecnicoApoyo5 = fields.Many2one('res.users', string='Tecnico de apoyo')
    location_id = fields.Many2one('crm.customer.location', string='Codigo', required=False,
                                  domain="[('location_type_id','=',location_type_id),('partner_id','=',partner_id)]")
    active = fields.Boolean("Active", default="True")
    cierre = fields.Boolean("Active", default="True")
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            if operator in positive_operators:
                locations = self.search([
                    '|',
                    ('partner_id', operator, name),
                    ('name', operator, name)
                ])
        else:
            locations = self.search(args, limit=limit)
        return locations.name_get()
    @api.multi
    def name_get(self):
        result = []
        for location in self:
            name = '[%s] %s' % (location.partner_id.name, location.name)
            result.append((location.id, name))
        return result
    # @api.constrains('name')
    # @api.one
    # def validarexistencia(self):
    #     if self.name:
    #         query = f"SELECT  name  FROM public.maintenance_request WHERE name = '{self.name}';"
    #         self._cr.execute(query)
    #         resul = self._cr.commit()
    #         if resul == self.name:
    #             raise ValidationError('El numero de servicio ya existe')
    #fin del codigo


    @api.multi
    def archive_equipment_request(self):
        self.write({'archive': True})

    @api.multi
    def reset_equipment_request(self):
        """ Reinsert the maintenance request into the maintenance pipe in the first stage"""
        first_stage_obj = self.env['maintenance.stage'].search([], order="sequence asc", limit=1)
        # self.write({'active': True, 'stage_id': first_stage_obj.id})
        self.write({'archive': False, 'stage_id': first_stage_obj.id})

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.user_id = self.equipment_id.technician_user_id if self.equipment_id.technician_user_id else self.equipment_id.category_id.technician_user_id
            self.category_id = self.equipment_id.category_id
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = self.equipment_id.maintenance_team_id.id

    @api.onchange('category_id')
    def onchange_category_id(self):
        if not self.user_id or not self.equipment_id or (self.user_id and not self.equipment_id.technician_user_id):
            self.user_id = self.category_id.technician_user_id

    def enviar_facturacion(self): #esta funcion envia a facturacion la notificacion
        if self.cierre == True:
            super(MaintenanceRequest, self).toggle_active()
            template_id = self.env.ref("maintenance.email_card_email").id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(self.id, force_send=True)
            self.cierre = False
        else:
            raise ValidationError(_("El mantenimiento se encuetra cerrado"))


    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        self = self.with_context(mail_create_nolog=True)
        request = super(MaintenanceRequest, self).create(vals)
        if request.owner_user_id or request.user_id:
            request._add_followers()
        if request.equipment_id and not request.maintenance_team_id:
            request.maintenance_team_id = request.equipment_id.maintenance_team_id
        request.activity_update()
        return request

    @api.multi
    def write(self, vals):
        # Overridden to reset the kanban_state to normal whenever
        # the stage (stage_id) of the Maintenance Request changes.
        if vals and 'kanban_state' not in vals and 'stage_id' in vals:
            vals['kanban_state'] = 'normal'
        res = super(MaintenanceRequest, self).write(vals)
        if vals.get('owner_user_id') or vals.get('user_id'):
            self._add_followers()
        if 'stage_id' in vals:
            self.filtered(lambda m: m.stage_id.done).write({'close_date': fields.Date.today()})
            self.activity_feedback(['maintenance.mail_act_maintenance_request'])
        if vals.get('user_id') or vals.get('schedule_date'):
            self.activity_update()
        if vals.get('equipment_id'):
            # need to change description of activity also so unlink old and create new activity
            self.activity_unlink(['maintenance.mail_act_maintenance_request'])
            self.activity_update()
        return res

    def activity_update(self):
        """ Update maintenance activities based on current record set state.
        It reschedule, unlink or create maintenance request activities. """
        self.filtered(lambda request: not request.schedule_date).activity_unlink(['maintenance.mail_act_maintenance_request'])
        for request in self.filtered(lambda request: request.schedule_date):
            date_dl = fields.Datetime.from_string(request.schedule_date).date()
            updated = request.activity_reschedule(
                ['maintenance.mail_act_maintenance_request'],
                date_deadline=date_dl,
                new_user_id=request.user_id.id or request.owner_user_id.id or self.env.uid)
            if not updated:
                if request.equipment_id:
                    note = _('Request planned for <a href="#" data-oe-model="%s" data-oe-id="%s">%s</a>') % (
                        request.equipment_id._name, request.equipment_id.id, request.equipment_id.display_name)
                else:
                    note = False
                request.activity_schedule(
                    'maintenance.mail_act_maintenance_request',
                    fields.Datetime.from_string(request.schedule_date).date(),
                    note=note, user_id=request.user_id.id or request.owner_user_id.id or self.env.uid)

    def _add_followers(self):
        for request in self:
            partner_ids = (request.owner_user_id.partner_id + request.user_id.partner_id).ids
            request.message_subscribe(partner_ids=partner_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    #Modificaciones para mantenimiento
    def action_send(self):
        value = {'stage_id': 'claim'}
        for request in self:
            if request.breakdown:
                value['request_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            request.write(value)

    # @api.multi
    # @api.onchange('location_type_id', 'partner_id', 'city_id')
    # def location_id_change(self):
    #     if not self.location_type_id and not self.partner_id and \
    #             not self.city_id:
    #         return
    #     domain = []
    #     if self.partner_id:
    #         domain.append(('partner_id', '=', self.partner_id.id))
    #     if self.location_type_id:
    #         domain.append(('location_type_id', '=', self.location_type_id.id))
    #     if self.city_id:
    #         domain.append(('city_id', '=', self.city_id.id))
    #     if len(domain) > 1:
    #             domain = ['&'] + domain
    #     locations = self.env['crm.customer.location']. \
    #         search(domain, limit=7000)
    #     location_ids = self.city_filter(locations)  # Retorna el Id de la Ciudad
    #     ids = [location.id for location in locations]
    #     return {'domain': {
    #         'location_id': [('id', 'in', ids)],
    #         'city_id': [('id', 'in', location_ids)]}
    #     }
    #esta funcion esta diseñada para cuando ingresen un excel guarde los datos como son
    @api.one
    @api.constrains('codigos')
    def codigos_excel(self):
        enditidad = self.partner_id.id
        tipo = self.location_type_id.id
        codig = self.codigos
        if not self.location_id:
            query = f"SELECT id, city_id FROM public.crm_customer_location WHERE code = '{codig}' AND location_type_id = '{tipo}' AND partner_id='{enditidad}';"
            self._cr.execute(query)
            data = self._cr.dictfetchall()
            txt = str(data)
            print(str(txt))
            z = txt.split(", ")
            x = str(z[0])
            y = str(z[1])
            y = y.split(": ")
            print('')
            y = y[1].split("}")
            x = x.split(": ")
            print('')
            x = x[1].split("}")
            self.location_id = x[0]
            self.city_id = y[0]

    def city_filter(self, locations):
        city_ids = []
        if locations:
            city_ids = [location.city_id.id for location in locations]
        return city_ids

    @api.onchange('location_id')
    def _onchange_partner_id(self):
        # self.location_type_id = self.location_id.location_type_id
        self.city_id = self.location_id.city_id


    @api.constrains('name')
    def _check_unique_number(self):
        if self.search_count([
            ('name', '=', self.name)
        ]) > 1:
            raise ValidationError(_("Atencion: Numero de servicio duplicado!"))

    #fin de las modificaciones



class MaintenanceTeam(models.Model):
    _name = 'maintenance.team'
    _description = 'Maintenance Teams'

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    member_ids = fields.Many2many('res.users', 'maintenance_team_users_rel', string="Team Members")
    color = fields.Integer("Color Index", default=0)
    request_ids = fields.One2many('maintenance.request', 'maintenance_team_id', copy=False)
    equipment_ids = fields.One2many('maintenance.equipment', 'maintenance_team_id', copy=False)

    # For the dashboard only
    todo_request_ids = fields.One2many('maintenance.request', string="Requests", copy=False, compute='_compute_todo_requests')
    todo_request_count = fields.Integer(string="Number of Requests", compute='_compute_todo_requests')
    todo_request_count_date = fields.Integer(string="Number of Requests Scheduled", compute='_compute_todo_requests')
    todo_request_count_high_priority = fields.Integer(string="Number of Requests in High Priority", compute='_compute_todo_requests')
    todo_request_count_block = fields.Integer(string="Number of Requests Blocked", compute='_compute_todo_requests')
    todo_request_count_unscheduled = fields.Integer(string="Number of Requests Unscheduled", compute='_compute_todo_requests')

    @api.one
    @api.depends('request_ids.stage_id.done')
    def _compute_todo_requests(self):
        self.todo_request_ids = self.request_ids.filtered(lambda e: e.stage_id.done==False)
        self.todo_request_count = len(self.todo_request_ids)
        self.todo_request_count_date = len(self.todo_request_ids.filtered(lambda e: e.schedule_date != False))
        self.todo_request_count_high_priority = len(self.todo_request_ids.filtered(lambda e: e.priority == '3'))
        self.todo_request_count_block = len(self.todo_request_ids.filtered(lambda e: e.kanban_state == 'blocked'))
        self.todo_request_count_unscheduled = len(self.todo_request_ids.filtered(lambda e: not e.schedule_date))

    @api.one
    @api.depends('equipment_ids')
    def _compute_equipment(self):
        self.equipment_count = len(self.equipment_ids)

class CrmCustomerLocation(models.Model):
    _name = 'crm.customer.location'
    _description = 'Equipment'

    name = fields.Char('Location Name', required=True)
    longitude = fields.Char('Longitude')
    latitude = fields.Char('Latitude')
    city_id = fields.Many2one('res.city', string='City')
    partner_id = fields.Many2one('res.partner', string='Partner Owner', \
        required=True)
    location_type_id = fields.Many2one('crm.customer.location.type', \
        string='Location Type', required=True)
    code = fields.Char('Code', required=True)
    region = fields.Selection([
        ('ant', "Antioquia"),
        ('bgta', "Bogota y Cundinamarca"),
        ('caribe', "Caribe"),
        ('centro', "Centro"),
        ('sur', "Sur")
    ], default='', required=False, string="Region")
    address = fields.Char('Address')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            if operator in positive_operators:
                locations = self.search([
                    '|',
                    ('code', operator, name),
                    ('name', operator, name)
                    ])
        else:
            locations = self.search(args, limit=limit)
        return locations.name_get()

    @api.multi
    def name_get(self):
        result = []
        for location in self:
            name = '[%s] %s'%(location.code, location.name)
            result.append((location.id, name))
        return result

    # @api.constrains('partner_id', 'code','location_type_id')
    # def _check_unicity(self):
    #     if self.search_count([
    #             ('partner_id', '=', self.partner_id.id),
    #             ('code', '=', self.code),
    #             ('location_type_id', '=', self.location_type_id.id)
    #         ]) > 1:
    #         raise ValidationError(_("Partner location duplicated!"))

class CrmBranchOffice(models.Model):
    _name = 'crm.customer.location.type'
    _description = 'Office Building'

    name = fields.Char('Name', required=True)


