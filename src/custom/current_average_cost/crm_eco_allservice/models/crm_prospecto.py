# -*- coding: utf-8 -*-

from openerp import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CrmProspectus(models.Model):
    _name = 'crm.prospectus'
    _description = 'CRM Prospectus'

    name = fields.Char('Name', required=True,
                       default='New')
    lead_id = fields.Many2one('crm.lead', 'Iniciativa')
    area_protect = fields.Integer('Areas a proteger', default=1)
    area_ids = fields.One2many('crm.areas', 'prospectus_id', 'Areas')
    place_implementation = fields.Selection(
        [('residencial', 'Residencial'),
         ('comercial', 'Comercial'),
         ('empresarial', 'Empresarial')
         ], 'Lugar de Implementación'
    )
    monitor_system_ids = fields.Many2many('crm.monitoring.system',
                                          string='Sistemas de Monitoreo')
    channel_ucp = fields.Selection(
        [('x4ch', 'x4CH'),
         ('x8ch', 'x8CH'),
         ('x12ch', 'x12CH'),
         ('x16ch', 'x16CH')
         ], 'Canales UCP'
    )
    is_monitor_system = fields.Boolean('Monitorear?')
    attc_file = fields.Binary('Archivo Adjunto', attachment=True)
    attc_file_ch = fields.Char('Attachment File Char')
    customer_need_id = fields.Many2one('product.category',
                                       string='Necesidades del Cliente')
    amount_money = fields.Integer('Cantidad de dinero a almacenar')
    #equipment_type_ids = fields.Many2many('project.spare.equipment.type',
    #                                      string='Type of Equipment')
    other_et = fields.Char('Otro Et')
    necessary_el_ids = fields.Many2many('crm.elements.light.eqm',
                                        string='Elementos')
    other_ne = fields.Char('Otro EN')
    color = fields.Selection([
        ('gris', 'Gris'),
        ('blanco', 'Blanco'),
        ('negro', 'Negro'),
        ('cafe', 'Cafe'),
        ('otro', 'otro'),
    ], string='Color')
    other_color = fields.Char('Otro Color')
    front = fields.Integer('Fondo')
    fund = fields.Integer('Frente')
    high = fields.Integer('Alto')
    value_type_ids = fields.Many2many('crm.value.type', string="Tipo de valor a almacenar")
    other_vt = fields.Char('Otros')
    is_armor_eqm = fields.Boolean('Desea Blindaje')
    blind_level = fields.Selection([
        ('lvl1', 'Level 1'),
        ('lvl2', 'Level 2'),
        ('lvl3', 'Level 3'),
    ], string='Nivel de blindaje')
    # Control de Acceso
    qty_access = fields.Integer('Cantidad de Accesos')

class CrmAreas(models.Model):
    _name = 'crm.areas'
    _description = 'CRM Areas'

    name = fields.Char('Nombre', required=True,
        default='New')
    prospectus_id = fields.Many2one('crm.prospectus',
        'Prospectus ID')
    sensors_total = fields.Integer('Sensores', default=0)
    wall_type = fields.Char('Tipo de Pared')
    door_type = fields.Char('Tipo de Puerta')
    proximity = fields.Integer('Proximidad', default=0)
    max_height = fields.Integer('Altura Mazima')
    description = fields.Text('Descripcion')
    photo = fields.Binary('Foto', attachment=True)
    #photo_ids = fields.Many2many('ir.attachment', string='Photos', attachment=True)
    #muk_ids = fields.Many2many('muk_dms.file', string='Photos Muk')
    #Control de acceso
    entry_room_ids = fields.Many2many('crm.entry.room', string='Entrada de Habitaciones')
    exit_room_ids = fields.Many2many('crm.exit.room', string='Salida de Habitaciones')

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.one
    @api.depends('prospectus_ids')
    def _prospectus_count(self):
        # _logger.critical('POR EL COUNT2')
        # self.prospectus_count = 1
        if self.prospectus_ids:
            self.prospectus_count = len(self.prospectus_ids)
        else:
            self.prospectus_count = 0

    prospectus_ids = fields.One2many('crm.prospectus','lead_id', string='Prospecto')
    prospectus_count = fields.Integer('Prospectus Count', compute='_prospectus_count')

class CrmValueType(models.Model):
    _name = 'crm.value.type'
    _description = 'crm.value.type'

    name = fields.Char('name', required=True)

class CrmExitRoom(models.Model):
    _name = 'crm.exit.room'
    _description = 'Salida de habitaciones'

    name = fields.Char('name', required=True)
    category_id = fields.Many2one('product.category','Category')

class CrmEntryRoom(models.Model):
    _name = 'crm.entry.room'
    _description = 'Entrada de habitaciones'

    name = fields.Char('name',  required=True)
    category_id = fields.Many2one('product.category','Category')


class CrmElements(models.Model):
    _name = 'crm.elements.light.eqm'
    _description = 'crm.elements.light.eqm'

    name = fields.Char('name', required=True)

class CrmMonitoringSystem(models.Model):
    _name = 'crm.monitoring.system'
    _description = 'CRM Monitoring System'

    name = fields.Char('Name', required=True,
        default='New')
    description = fields.Char('Description')
    prospectus_id = fields.Many2one('crm.prospectus', 'Prospectus ID')
