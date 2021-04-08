# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.http import request

class ks_file_preview(http.Controller):
    # Controller: Get the file details
    @http.route(['/get/record/details'], type='json', auth="public", methods=['POST'], website=True)
    def GetRecordData(self,res_id, model, size, res_field, **kw):
        data_file = {}
        data = request.env['ir.attachment'].sudo().search([('res_model', '=', model), ('res_id', '=', res_id), ('res_field', '=', res_field)])
        div = 2014
        if size[-2:] == 'Kb' or size[-2:] == 'kb':
            div = 1024
        elif size[-2:] == 'Mb' or size[-2:] == 'mb':
            div = 1024*1024
        elif size[-5:] == 'bytes' or size[-5:] == 'Bytes':
            div = 1
            size = size[:-3]

        for d in data:
            if float(size[:-3]) == round(d.file_size/div, 2):
                data_file = {
                    'name': d.name or d.dispay_name,
                    'id': d.id,
                    'type': d.mimetype,
                }
                break

        return data_file
