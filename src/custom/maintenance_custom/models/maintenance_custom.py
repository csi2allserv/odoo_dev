# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError



class maintenanceIssues(models.Model):
    _inherit = "maintenance.request"

    #@api.model
    #def _default_partner_issue(self):
    #    return self.env['crm.customer.location.type'].search([('name', '=', 'Oficina')], limit=1)

    location_type_id = fields.Many2one('crm.customer.location.type',string='Tipo de Ubicacion')
    location_id = fields.Many2one('crm.customer.location', string='Codigo', required=True)
    city_id = fields.Many2one('res.city', string='Ciudad')

    categs_ids = fields.Many2many('product.category',
                                  string='categorias',
                                  help='Puede agregar varias categorias')
    partner_id = fields.Many2one(domain=[
        ('is_company', '=', True),
        ('customer', '=', True)
    ], )
    contact_id = fields.Many2one('res.partner', string='Contact')

    branch_type = fields.Selection([
        ('office', 'Oficina'),
        ('atm', 'cajero'),
        ('edi', 'Edificio')
    ], default='office', required=False, string='location')

    request_type = fields.Selection([
        ('macor', "Mantenimiento Correctivo"),
        ('mapreven', "Mantenimiento Preventivo")
    ], default='macor', required=True, string="Tipo")


    @api.multi
    def real_location_id_change(self, location_id):
        if not location_id:
            return
        res_dict = {}
        location_id = self.env['crm.customer.location']. \
            search([('id', '=', location_id)])
        contacts = self.env['res.partner'] \
            .search([('parent_id', '=', location_id.partner_id.id)])
        contact_ids = [contact.id for contact in contacts]
        res_dict['domain'] = {'contact_id': [('id', 'in', contact_ids)]}
        res_dict['value'] = {'city_id': location_id.city_id.id,
                             'location_type_id': location_id.partner_id.id,
                             'partner_id': location_id.partner_id.id}
        if len(contact_ids) == 1:
            res_dict['value']['contact_id'] = contact_ids[0]
        return res_dict

    @api.multi
    def name_project_issue_change(self, request_type=None, categs_ids=None, \
                                  location_type_id=None,city_id=None,partner_id=None, location_id=None):
        res = self.set_name_issue(request_type,categs_ids, \
                                  location_type_id,city_id,partner_id,location_id)
        if res: return{'value': res}

    @api.multi
    def partner_id_change(self, request_type=None, categs_ids=None, \
                          location_type_id=None, city_id=None, partner_id=None):
        if not partner_id:
            return
        res_dict = {}
        partner_id = self.env['res.partner'].search(
            [('id', '=', partner_id)])
        contacts = self.env['res.partner']\
            .search([('parent_id', '=', partner_id)])
        contact_ids = [contact.id for contact in contacts]
        res_dict['domain'] = {'contact_id': [('id', 'in', contact_ids)]}
        res = self.set_name_issue(request_type,categs_ids,\
                                  location_type_id,city_id,partner_id)
        if res:
            res_dict['value'] = res
        if contact_ids:
            if len(contact_ids) == 1:
                res_dict['value']['contact_id'] = contact_ids[0]
        else:
            res_dict['value']["contact_id"] = False
        return res_dict

    def  set_name_issue(self, request_type=None, categs_ids=None,\
                        location_type_id=None, city_id=None,partner_id=None,location_id=None):
        if not request_type and not categs_ids \
            and not partner_id and not location_type_id \
            and not city_id:
            return
        name = []
        if request_type:
            request_type_name = dict(self._columns['request_type'].selection)\
                .get(request_type)
            name.append(request_type_name)
        if location_type_id:
            location_type = self.env['crm.customer.location.type'].search(\
                [('id', '=', location_type_id)])
            name.append(location_type.name)
        if location_id:
            location = self.env['crm.customer.location'].\
                search([('id', '=', location_id)])
            name.append(location.code)
        if city_id:
            city = self.env['res.city'].search(\
                [('id', '=', city_id)])
            name.append(city.city)
        if len(name) > 0:
            clean_name(name)
            name = ' '.join(name)
            return {'name': name}

def clean_name(name):
    if len(name) > 0:
        try:
            name.remove(False)
        except:
            pass
        try:
            name.remove(None)
        except:
            pass





