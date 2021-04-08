# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlwt
import base64
from io import StringIO
from odoo import api, fields, models, _
import platform


class PurchaseReportOut(models.Model):
    _name = 'expense.report.out'
    _description = 'expense order report'

    purchase_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Purchase Excel Report', readonly=True)
    purchase_work = fields.Char('Name', size=256)
    file_names = fields.Binary('Purchase CSV Report', readonly=True)


class WizardWizards(models.Model):
    _name = 'wizard.reportes'
    _description = 'purchase wizard'
    
    # purchase order excel report button actions
    @api.multi
    def action_purchase_report(self):
        # XLS report
        custom_value = {}
        label_lists = ['Tipo Documento Beneficiario', 'Nit Beneficiario', 'Nombre Beneficiario', 'Tipo Transaccion', 'Codigo Banco', 'No Cuenta Beneficiario', 'Email', 'Documento Autorizado', 'Referencia',
                       'OficinaEntrega', 'ValorTransaccion', 'Fecha de aplicación']
        order = self.env['hr.expense.sheet'].browse(self._context.get('active_ids', list()))
        #ordershet = self.env['hr.expense.sheet'].browse(self._context.get('active_ids', list()))
        workbook = xlwt.Workbook()
        
        for obj in order:
            purchase = []
            for lines in obj:
                product = {}
                product['origin'] = lines.origin.name
                product['default_code'] = lines.default_code
                purchase.append(product)

                custom_value['products'] = purchase
                custom_value['origin'] = lines.origin.name
                custom_value['default_code'] = obj.default_code
                custom_value['user_id'] = obj.name
                custom_value['company_id'] = obj.company_id.vat
                
        
        
        style0 = xlwt.easyxf(
            'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz right;',
            num_format_str='#,##0.00')
        style1 = xlwt.easyxf(
            'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz left;',
            num_format_str='#,##0.00')
        style2 = xlwt.easyxf('font:height 250,bold True;borders:left thin, right thin, top thin, bottom thin;', num_format_str='#,##0.00')    
        style5 = xlwt.easyxf(
            'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;align: horiz center;',
            num_format_str='#,##0')
        style6 = xlwt.easyxf(
            'font: name Times New Roman bold on;borders:left thin, right thin, top thin, bottom thin;',
            num_format_str='#,##0.00')
        sheet = workbook.add_sheet("objname")
        #sheet = workbook.add_sheet(rec.name)
            

        sheet.write(0, 0, 'NIT PAGADOR', style1)
        sheet.write(0, 1, 'TIPO DE PAGO', style1)
        sheet.write(0, 2, 'APLICACIÓN', style1)
        sheet.write(0, 3, 'SECUENCIA DE ENVÍO', style1)
        sheet.write(0, 4, 'NRO CUENTA A DEBITAR', style1)
        sheet.write(0, 5, 'TIPO DE CUENTA A DEBITAR', style1)
        sheet.write(0, 6, 'DESCRIPCÓN DEL PAGO', style1)
        sheet.write(2, 0, 'Tipo Documento Beneficiario', style1)
        sheet.write(2, 1, 'Nit Beneficiario', style1)
        sheet.write(2, 2, 'Nombre Beneficiario', style1)
        sheet.write(2, 3, 'Tipo Transaccion', style1)
        sheet.write(2, 4, 'Código Banco', style1)
        sheet.write(2, 5, 'No Cuenta Beneficiario', style1)
        sheet.write(2, 6, 'Email', style1)
        sheet.write(2, 7, 'Documento Autorizado', style1)
        sheet.write(2, 8, 'Referencia', style1)
        sheet.write(2, 9, 'OficinaEntrega', style1)
        sheet.write(2, 10,'ValorTransaccion', style1)
        sheet.write(2, 11,'Fecha de aplicación', style1)

        #i=4
        #for n in custom_value['products']:
        #    i=i+1
        #    sheet.write(i, 3, n['origin'], style6)
        #    sheet.write(i, 4, n['default_code'], style0)
        #    n += 1

        n = 11; m=10; i = 1
        for product in custom_value['products']:
            sheet.write(n, 1, i, style5)  
            sheet.write_merge(n, n, 2, 3, product['origin'], style6)      
            sheet.write_merge(n, n, 4, 5, product['default_code'], style0)                        
            n += 1; m +=1; i += 1
        #n = 11; m=10; i = 1
        #for product in custom_value['products']: 
        #    sheet.write_merge(n, n, 2, 3, product['origin'], style6)      
            #sheet.write(3, 1, product['default_code'], style0)

        # CSV report

        datas = []
        for values in order:
            for value in values:
                if value:
                    item = [
                            str(value.categ_id.name or ''),                       
                            str(value.origin.name or ''),
                            str(value.applicant.name or ''),
                            str(value.company_id.name or ''),                     
                            ] 
                    datas.append(item)    
            
        output = StringIO()
        label = ','.join(label_lists)               
        output.write(label)         
        output.write("\n")

        for data in datas:       
            record = ';'.join(data)
            output.write(record)
            output.write("\n")
        data = base64.b64encode(bytes(output.getvalue(),"utf-8"))


        if platform.system() == 'Linux':
            filename = ('/tmp/Purchase Report' + '.xls')
        else:
            filename = ('Purchase Report' + '.xls')

        workbook.save(filename)
        fp = open(filename, "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)
                        
# Files actions         
        attach_vals = {
                'purchase_data': 'Purchase Report'+ '.xls',
                'file_name': out,
                'purchase_work':'Purchase'+ '.csv',
                'file_names':data,
            } 
            
        act_id = self.env['expense.report.out'].create(attach_vals)
        fp.close()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'expense.report.out',
        'res_id': act_id.id,
        'view_type': 'form',
        'view_mode': 'form',
        'context': self.env.context,
        'target': 'new',
        }
































