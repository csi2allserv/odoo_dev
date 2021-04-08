#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime
from odoo.exceptions import ValidationError

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class purchaseCardReport(models.AbstractModel):
    _name = 'report.odoo_mo_monthlypurchase.template_id11'

    def _get_report_values(self, docids, data=None):
        lines=data.get('lines',[])
        docargs = {
            'lines': lines,
        }
        return docargs



class Xlsl_report_get(models.AbstractModel):
    _name = 'report.odoo_mo_monthlypurchase.xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        listss = []
        product_list_ids = []
        for rec in  self.env['purchase.report'].search([]):
            if (rec.product_id.id in product_list_ids):
                continue
            else:
                product_list_ids.append(rec.product_id.id)

        for rec in product_list_ids:
            for i in range(1, 13, 1):
                startgdate = str(i) + '/1/' + str(lines.year_for_xls.year) + ' 19:12:57'
                enddate = str(i + 1) + '/1/' + str(lines.year_for_xls.year) + ' 19:12:57'
                total = 0
                if (i != 12):
                    for object_purchase in self.env['purchase.report'].search(
                        ['&', ('product_id', '=', rec), ('date_order', '>', startgdate),
                         ('date_order', '<', enddate)]):
                        total = total + object_purchase.unit_quantity
                    listss.append(total)
                else:
                    enddate = '01/1/' + str(lines.year_for_xls.year + 1) + ' 19:12:57'
                    for object_purchase in self.env['purchase.report'].search(
                        ['&', ('product_id', '=', rec), ('date_order', '>', startgdate),
                         ('date_order', '<', enddate)]):
                        total = total + object_purchase.unit_quantity
                    listss.append(total)
        n = 12
        listss = [listss[i * n:(i + 1) * n] for i in range((len(listss) + n - 1) // n)]
        def Extract(l, lst):
            return [item[l] for item in lst]
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet('Product purchase   For ' + str(lines.year_for_xls))
        sheet.write('', '', bold)
        sheet.merge_range('E1:F1', 'Jan', bold)
        sheet.write('E2', 'quantity', bold)
        sheet.write('F2', 'Amount', bold)
        sheet.merge_range('G1:H1', 'Feb', bold)
        sheet.write('G2', 'quantity', bold)
        sheet.write('H2', 'Amount', bold)
        sheet.merge_range('I1:J1', 'Mar', bold)
        sheet.write('I2', 'quantity', bold)
        sheet.write('J2', 'Amount', bold)
        sheet.merge_range('K1:L1', 'Apr', bold)
        sheet.write('K2', 'quantity', bold)
        sheet.write('L2', 'Amount', bold)
        sheet.merge_range('M1:N1', 'May', bold)
        sheet.write('M2', 'quantity', bold)
        sheet.write('N2', 'Amount', bold)
        sheet.merge_range('O1:P1', 'Jun', bold)
        sheet.write('O2', 'quantity', bold)
        sheet.write('P2', 'Amount', bold)
        sheet.merge_range('Q1:R1', 'Jul', bold)
        sheet.write('Q2', 'quantity', bold)
        sheet.write('R2', 'Amount', bold)
        sheet.merge_range('S1:T1', 'Aug', bold)
        sheet.write('S2', 'quantity', bold)
        sheet.write('T2', 'Amount', bold)
        sheet.merge_range('U1:V1', 'Sep', bold)
        sheet.write('U2', 'quantity', bold)
        sheet.write('V2', 'Amount', bold)
        sheet.merge_range('W1:X1', 'Oct', bold)
        sheet.write('W2', 'quantity', bold)
        sheet.write('X2', 'Amount', bold)
        sheet.merge_range('Y1:Z1', 'Nov', bold)
        sheet.write('Y2', 'quantity', bold)
        sheet.write('Z2', 'Amount', bold)
        sheet.merge_range('AA1:AB1', 'Dec', bold)
        sheet.write('AA2', 'quantity', bold)
        sheet.write('AB2', 'Amount', bold)
        sheet.merge_range('AC1:AD1', 'TOTAL', bold)
        sheet.write('AC2', 'quantity', bold)
        print(listss)
        row = 2
        col = 0
        i = 3
        counter = 0
        for rec in listss:
            total_sum=0
            merge_cell = 'A' + str(i) + 'B' + str(i) + 'C' + str(i) + ':D' + str(i)
            sheet.merge_range(merge_cell, str(
                self.env['product.product'].search([('id', '=', product_list_ids[counter])]).name), bold)
            sheet.write(row, col + 4, listss[counter][0])
            sheet.write(row, col + 5, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][0]))
            sheet.write(row, col + 6, listss[counter][1])
            sheet.write(row, col + 7, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][1]))
            sheet.write(row, col + 8, listss[counter][2])
            sheet.write(row, col + 9, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][2]))
            sheet.write(row, col + 10, listss[counter][3])
            sheet.write(row, col + 11, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][3]))
            sheet.write(row, col + 12, listss[counter][4])
            sheet.write(row, col + 13, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][4]))
            sheet.write(row, col + 14, listss[counter][5])
            sheet.write(row, col + 15, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][5]))
            sheet.write(row, col + 16, listss[counter][6])
            sheet.write(row, col + 17, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][6]))
            sheet.write(row, col + 18, listss[counter][7])
            sheet.write(row, col + 19, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][7]))
            sheet.write(row, col + 20, listss[counter][8])
            sheet.write(row, col + 21, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][8]))
            sheet.write(row, col + 22, listss[counter][9])
            sheet.write(row, col + 23, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][9]))
            sheet.write(row, col + 24, listss[counter][10])
            sheet.write(row, col + 25, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][10]))
            sheet.write(row, col + 26, listss[counter][11])
            sheet.write(row, col + 27, str(
                (self.env['product.product'].search([('id', '=', product_list_ids[counter])]).list_price) *
                listss[counter][11]))
            sheet.write(row, col + 28, sum(listss[counter]))

            row += 1
            i += 1
            counter += 1


