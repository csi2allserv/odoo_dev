# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ejempp(models.Model):
    _name = 'ejempp.ejempp'

    name = fields.Char(string='Nombre',required=True)
    value = fields.Integer(string='Documento',required=True,default=0)
    date = fields.Date(string='fehca de ingreso')

