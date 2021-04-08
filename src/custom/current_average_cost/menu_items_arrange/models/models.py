# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.

from odoo import models, fields, api

STATES = [
    ('name_asen', 'Name Ascending'),
    ('name_desc', 'Name Descending'),
    ('create_date_asen', 'App Installed Date Ascending'),
    ('create_date_desc', 'App Installed Date Descending'),
    ('sequence_asen', 'Sequence Number Ascending'),
    ('sequence_desc', 'Sequence Number Descending'),

]

class ResConfigSettingsMenu(models.TransientModel):
    _inherit = 'res.config.settings'
    config_menu = fields.Selection(string="Sort Menu Apps By:",config_parameter='menu_items_arrange_config_menu', selection=STATES, store=True)

    def set_values(self):
        super(ResConfigSettingsMenu, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('config_menu', (self.config_menu or '').strip())
        
    @api.model
    def get_values(self):
        res = super(ResConfigSettingsMenu, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            config_menu=get_param('config_menu', default=''),
        )
        return res

    @api.onchange('config_menu')
    def change_sequence(self):
        if self.config_menu == 'name_asen':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="name")
            count = 10
            for each in records:
                each.write({'sequence':count})
                count = count + 1
        
        elif self.config_menu == 'create_date_asen':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="create_date")
            count = 10
            for each in records:
                each.write({'sequence':count})
                count = count + 1

        elif self.config_menu == 'sequence_asen':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="sequence")
            for each in records:
                if each.old_seq:
                    each.sequence = each.old_seq
        elif self.config_menu == 'name_desc':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="name desc")
            count = 10
            for each in records:
                each.write({'sequence':count})
                count = count + 1
        
        elif self.config_menu == 'create_date_desc':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="create_date desc")
            count = 10
            for each in records:
                each.write({'sequence':count})
                count = count + 1

        elif self.config_menu == 'sequence_desc':
            records = self.env['ir.ui.menu'].search([('parent_id','=',False)],order="sequence desc")
            for each in records:
                if each.old_seq:
                    each.sequence = each.old_seq


class menu_items_arrange(models.Model):
    _inherit  = 'ir.ui.menu'
    
    old_seq = fields.Integer(string="Old Sequence",compute='_copy_sequence',store=True)

    @api.depends('sequence')
    def _copy_sequence(self):
        for each in self:
            if each.old_seq == False or each.old_seq == 0:
                each.old_seq = each.sequence
            else:
                return False

    
    


