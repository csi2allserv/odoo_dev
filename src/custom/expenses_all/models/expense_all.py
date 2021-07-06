# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp


class HrExpense(models.Model):

    _inherit = ['hr.expense.sheet']
    _description = "Expense"


    categ_id = fields.Many2one('expense.all', string='Tipo', readonly= True, states={'draft': [('readonly', False)], 'finalizado': [('readonly', False)]})
    applicant = fields.Many2one('res.users', string='Solicitante', readonly= True, states={'draft': [('readonly', False)]})
    
    default_code = fields.Char(
        readonly=True,
        default='/',
        track_visibility='onchange',
        help="Set to '/' and save if you want a new internal reference "
             "to be proposed."
    )
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', track_sequence=1, index=True, readonly= True, states={'draft': [('readonly', False)]},
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    city_id = fields.Many2one('res.city', string='Ciudad', readonly= True, states={'draft': [('readonly', False)]})
    location_id = fields.Many2one('crm.customer.location', \
                                  string='Codigo', readonly= True, states={'draft': [('readonly', False)]} )



    @api.onchange('origin')
    def _onchange_partner_id(self):
        self.partner_id = self.origin.partner_id
        self.city_id = self.origin.city_id
        self.location_id = self.origin.location_id
    
    @api.model
    def create(self, vals):
        if 'default_code' not in vals or vals['default_code'] == '/':
            categ_id = vals.get("categ_id")
            template_id = vals.get("product_tmpl_id")
            categ = sequence = False
            if categ_id:
                # Created as a product.product
                categ = self.env['expense.all'].browse(categ_id)
            elif template_id:
                # Created from a product.template
                template = self.env["hr.expense.sheet"].browse(template_id)
                categ = template.categ_id
            if categ:
                sequence = categ.sequence_id
            if not sequence:
                sequence = self.env.ref('expense_all.seq_product_auto')
            vals['default_code'] = sequence.next_by_id()
        return super().create(vals)

    @api.multi
    def write(self, vals):
        """Para asignar una nueva referencia interna, simplemente escriba '/' en el campo.
        Tenga en cuenta que esto depende del usuario, si se cambia la categoría del producto,
        necesitará escribir '/' en la referencia interna para forzar
        reasignación"""
        if vals.get('default_code', '') == '/':
            product_category_obj = self.env['product.category']
            for product in self:
                category_id = vals.get('categ_id', product.categ_id.id)
                category = product_category_obj.browse(category_id)
                sequence = category.exists() and category.sequence_id
                if not sequence:
                    sequence = self.env.ref(
                        'product_sequence.seq_product_auto')
                ref = sequence.next_by_id()
                vals['default_code'] = ref
                if len(product.product_tmpl_id.product_variant_ids) == 1:
                    product.product_tmpl_id.write({'default_code': ref})
                super(HrExpense, product).write(vals)
            return True
        return super().write(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        if self.default_code and 'default_code' not in default:
            default.update({
                'default_code': self.default_code + _('-copy'),
            })
        return super().copy(default)


class hrExpenseAll(models.Model):

    _name = "expense.all"

    name = fields.Char('Nombre de la categoria')
    code_prefix = fields.Char(
        string="Prefijo de Referencia",
        help="Prefijo utilizado para generar la referencia interna para productos "
             "creado con esta categoría. Si está en blanco el "
             "se usará la secuencia predeterminada.",
    )
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence", string="Product Sequence",
        help="Este campo contiene la información relacionada con la numeración "
             "de los asientos de este diario.",
        copy=False, readonly=False,
    )
    product_id = fields.Many2many('product.product', string='Product')


    @api.model
    def _prepare_ir_sequence(self, prefix):
        """Prepare los vals para crear la secuencia.
        : prefijo param: una cadena con el prefijo de la secuencia.
        : return: un dict con los valores..
        """
        vals = {
            "name": "Product " + prefix,
            "code": "product.product - " + prefix,
            "padding": 5,
            "prefix": prefix,
            "company_id": False,
        }
        return vals

    @api.multi
    def write(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            for rec in self:
                if rec.sequence_id:
                    rec.sudo().sequence_id.prefix = prefix
                else:
                    seq_vals = self._prepare_ir_sequence(prefix)
                    rec.sequence_id = self.env["ir.sequence"].create(seq_vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            seq_vals = self._prepare_ir_sequence(prefix)
            sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().create(vals)
