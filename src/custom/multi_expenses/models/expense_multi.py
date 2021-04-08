

from odoo import api, fields, models, _
from odoo import _, api, exceptions, fields, models


class hrExpenseMulti(models.Model):

    _name = 'hr.expense.multi'


    description = fields.Char('Descripcion', readonly= False)
    valor = fields.Float('Valor', readonly= False)
    product_id = fields.Many2many('product.product', string='Productos', domain=[('can_be_expensed', '=', True)], required=True)


