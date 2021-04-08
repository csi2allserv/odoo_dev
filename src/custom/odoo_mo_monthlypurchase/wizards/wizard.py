# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Wizard(models.TransientModel):
    _name = 'odoo_mo.monthly_purchases'

    date_from = fields.Date(string="Date From", required=False)
    date_to = fields.Date(string="Date To", required=False)
    use_pdf = fields.Boolean(string="Use Pdf", )
    categ_id = fields.Many2many(comodel_name="product.category", string="Select Category", required=False, )
    year_for_xls = fields.Date(string="Select Year For Xls", required=False, default=fields.Date.context_today)
    lines = fields.One2many(comodel_name="odoo_mo.mpurchases_template", inverse_name="wiz_id", string="Data",
                            readonly=True)

    def _get_lines(self):

        if not self.use_pdf:
            return True
        if self.categ_id:
            domain = tuple(self.categ_id.ids) if len(self.categ_id) > 1 else (self.categ_id.ids[0], 0)
            query = ("""


            SELECT purchase_report.product_id as pro_name,purchase_report.category_id as pro_categ,unit_quantity,purchase_report.date_order as odate
                 FROM purchase_report
                join product_product on product_product.id = purchase_report.product_id
                join product_category on product_category.id = purchase_report.category_id
                where  date_order  >=\'{date_form}\' and  date_order <=\'{date_to}\'   and purchase_report.category_id in {categ_ids}
               GROUP BY pro_categ,pro_name,unit_quantity,purchase_report.date_order
                ORDER BY pro_categ,purchase_report.unit_quantity
                                 """.format(date_form=self.date_from, date_to=self.date_to, categ_ids=domain))
        else:
            query = ("""

            SELECT purchase_report.product_id as pro_name,purchase_report.category_id as pro_categ,unit_quantity,purchase_report.date_order as odate
                 FROM purchase_report
                join product_product on product_product.id = purchase_report.product_id
                join product_category on product_category.id = purchase_report.category_id
                where purchase_report.date_order  >=\'{date_form}\' and  purchase_report.date_order <=\'{date_to}\'
                GROUP BY pro_categ,pro_name,unit_quantity,purchase_report.date_order
                ORDER BY pro_categ,purchase_report.unit_quantity
                             """.format(date_form=self.date_from, date_to=self.date_to))

        self._cr.execute(query)
        lines = self._cr.dictfetchall()
        return lines

    def preview(self):
        self.lines = [(5, 0, 0)]
        line_list = []
        lines = self._get_lines()

        for line in lines:
            line_list.append((0, 0, {
                'categ': self.env['product.category'].search([('id', '=', line.get('pro_categ'))]).name,
                'qty': str(line.get('unit_quantity')),
                'product_name': self.env['product.product'].search([('id', '=', line.get('pro_name'))]).name,
                'odate': str(line.get('odate')),
            }))
        self.lines = line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "odoo_mo.monthly_purchases",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Monthly Purchases',
            'target': 'new'
        }

    def print_pdf(self):
        data = {}
        lines = self._get_lines()
        data['lines'] = lines
        print(lines)

        return self.env.ref('odoo_mo_monthlypurchase.pdf_reportid11').report_action([], data=data)

    def print_excel(self):
        data = {}
        lines = self._get_lines()
        data['lines'] = lines
        print(lines)

        return self.env.ref('odoo_mo_monthlypurchase.xls_reportid22').report_action([], data=data)


class Template(models.TransientModel):
    _name = 'odoo_mo.mpurchases_template'

    odate = fields.Char(string="Order Date", required=False, )
    categ = fields.Char(string="Category", required=False, )
    qty = fields.Char(string="Qty", required=False, )
    product_name = fields.Char(string="Product", required=False, )

    wiz_id = fields.Many2one(comodel_name="odoo_mo.monthly_purchases")
