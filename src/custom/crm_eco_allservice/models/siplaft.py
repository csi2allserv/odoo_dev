# -*- codig: utf-8 -*-

from openerp import models, fields, api


class siplaft(models.Model):
    _name = 'crm.siplaft'
    _inherit = ['mail.thread']

    lead_id = fields.Many2one('crm.lead', 'Lead ID')
    sop_proc = fields.Binary('Soporte Procuraduria', attachment=True)
    sop_proc_ch = fields.Char('Nombre de Archivo')
    sop_contra = fields.Binary('Soporte Contraloria', attachment=True)
    sop_contra_ch = fields.Char('Nombre de Archivo')
    sop_rues = fields.Binary('Soporte RUES', attachment=True)
    sop_rues_ch = fields.Char('Nombre de Archivo')
    rut = fields.Binary('RUT', attachment=True)
    rut_ch = fields.Char('Nombre de Archivo')
    cam_com = fields.Binary('Cámara de Comercio', attachment=True)
    cam_com_ch = fields.Char('Nombre de Archivo')
    cust_study = fields.Binary('Estudio de Cliente', attachment=True)
    cust_study_ch = fields.Char('Nombre de Archivo')
    check_list = fields.Binary('Lista de Chequeo', attachment=True)
    check_list_ch = fields.Char('Nombre de Archivo')
    fecha_proc = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    fecha_contra = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    fecha_rues = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    date_rut = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    date_cam_com = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    date_cust_study = fields.Date('Fecha de Adjunto', default=fields.Date.today())
    date_check_list = fields.Date('Fecha de Adjunto', default=fields.Date.today())

    obser = fields.Text()
    user_id = fields.Many2one('res.users', domain=['|', ('salesman', '=', True), ('coordinator', '=', True)])
    # Campo que trae el nombre de la oportunidad, según la relación
    # name = fields.Char(related="lead_id.sec", readonly=True)

    # Campo de estado para el workflow
    state = fields.Selection([
        ('draft', "Borrador"),
        ('pending', "Pendiente"),
        ('confirmed', "Aprobado"),
        ('cancel', "Cancelado"),
        ('closed', "Cerrado"),
    ])

    # campo que almacena el valor de la compañia actual
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('crm.siplaft'))

    # def get_signup_url(self):
    #    signup_url = self.env['ir.config_parameter'].get_param('web.base.url')

    # Acción que asigna los estados del workflow
    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

    @api.multi
    def action_close(self):
        self.state = 'closed'

    @api.multi
    @api.model
    def action_mail_custom(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data'].search([])

        try:
            template_id = ir_model_data.get_object_reference('crm_eco_allservice', 'custom_template_siplaft_basico')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'crm.siplaft',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })

        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    siplaft_ids = fields.One2many('crm.siplaft', 'lead_id', string='Basic Siplaft')
    siplaft_count = fields.Integer('Siplaft Count', compute='_siplaft_count')
    # Funcion que lleva el conteo de los siplaft basicos
    @api.one
    @api.depends('siplaft_ids')
    def _siplaft_count(self):
        if self.siplaft_ids:
            self.siplaft_count = len(self.siplaft_ids)
        else:
            self.siplaft_count = 0


