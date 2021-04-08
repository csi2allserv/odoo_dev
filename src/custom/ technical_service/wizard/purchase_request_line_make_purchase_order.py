# Copyright 2018-2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).


from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime


class MaintenanceRequestLineMakeMaintenanceOrder(models.TransientModel):
    _name = "maintenance.request.line.make.maintenance.order"
    _description = "Maintenance Request Line Make Maintenance Order"

    supplier_id = fields.Many2one('res.partner', string='Supplier',
                                  domain=[('supplier', '=', True),
                                          ('is_company', '=', True)])
    item_ids = fields.One2many(
        'maintenance.request.line.make.maintenance.order.item',
        'wiz_id', string='Items')
    activity_type_id = fields.Many2one('mail.activity.type', string='Actividad')
    schedule_date = fields.Date('Fecha vencimiento', related='item_ids.schedule_date', readonly=False)
    purchase_order_id = fields.Many2one('maintenance.request',
                                        string='Purchase Order',
                                        domain=[('state', '=', 'draft')])
    sync_data_planned = fields.Boolean(
        string="Merge on PO lines with equal Scheduled Date")
    user_id = fields.Many2one('res.users', string='Technician')

    @api.model
    def _prepare_item(self, line):
        return {
            'line_id': line.id,
            'maintenance_type': line.maintenance_type,
            'city_id': line.city_id.id,
            'name': line.name or line.request_id,
            'partner_id': line.partner_id.id,
            'location_id': line.location_id.id,
            'schedule_date': line.schedule_date
        } 
    @api.model
    def check_group(self, request_lines):
        if len(list(set(request_lines.mapped('partner_id')))) > 1:
            raise UserError(
                _('You cannot create a single purchase order from '
                  'purchase requests that have different procurement group.'))

    @api.model
    def get_items(self, request_maintenance_line_ids):
        request_line_obj = self.env['maintenance.request']
        items = []
        request_lines = request_line_obj.browse(request_maintenance_line_ids)
        self.check_group(request_lines)
        for line in request_lines:
            items.append([0, 0, self._prepare_item(line)])
        return items   

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get('active_model', False)
        request_maintenance_line_ids = []
        if active_model == 'maintenance.request':
            request_maintenance_line_ids += self.env.context.get('active_ids', [])
        elif active_model == 'maintenance.request':
            request_ids = self.env.context.get('active_ids', False)
            request_maintenance_line_ids += self.env[active_model].browse(
                request_ids).mapped('line_ids.id')
        if not request_maintenance_line_ids:
            return res
        res['item_ids'] = self.get_items(request_maintenance_line_ids)
        request_lines = self.env['maintenance.request'].browse(
            request_maintenance_line_ids)
        #supplier_ids = request_lines.mapped('supplier_id').ids
        #if len(supplier_ids) == 1:
        #    res['supplier_id'] = supplier_ids[0]
        return res

    @api.model
    def _prepare_purchase_order(self, group_id,origin, city_id, location_id, partner_id, code, name, description, schedule_date):
        #if not self.supplier_id:
        #    raise UserError(
        #        _('Enter a supplier.'))
        supplier = self.supplier_id
        data = {
            'origin': origin,
            'partner_id': partner_id.name,
            'name': name,
            'city_id': city_id.id,
            'location_id': location_id.id,
            'code': code,
            'description': description,
            'schedule_date': schedule_date
            }
        return data

    @api.multi
    def make_purchase_order(self):
        res = []
        purchase_obj = self.env['technical.maintenance']
        po_line_obj = self.env['maintenance.request']
        purchase = False

        for item in self.item_ids:
            line = item.line_id
            if self.purchase_order_id:
                purchase = self.purchase_order_id
            if not purchase:
                po_data = self._prepare_purchase_order(
                    line.name,
                    line.user_id,
                    line.city_id,
                    line.location_id,
                    line.partner_id,
                    line.name,
                    line.code,
                    line.description,
                    line.schedule_date)
                purchase = purchase_obj.create(po_data)
                res.append(purchase.id)
        
        return {
            'domain': [('id', 'in', res)],
            'name': _('Servicio Creado'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'technical.maintenance',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }



class MaintenanceRequestLineMakeMaintenanceOrderItem(models.TransientModel):
    _name = "maintenance.request.line.make.maintenance.order.item"
    _description = "Maintenance Request Line Make Maintenance Order Item"

    wiz_id = fields.Many2one(
        'maintenance.request.line.make.maintenance.order',
        string='Wizard', required=True, ondelete='cascade',
        readonly=True)
    line_id = fields.Many2one('maintenance.request',
                              string='maintenance Request Line')
    request_id = fields.Many2one('purchase.request',
                                 string='Purchase Request',
                                 readonly=False)
    city_id = fields.Many2one('res.city', string='Ciudad')
    name = fields.Char(string='Numero de servicio', required=True)
    code = fields.Char(string='Codigo')
    product_qty = fields.Float(
        string='Quantity to purchase',
        digits=dp.get_precision('Product Unit of Measure'))
    partner_id = fields.Many2one('res.partner', string='Customer')
    location_id = fields.Many2one('crm.customer.location', string='Tipo ubicación')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Proceso')
    description = fields.Text('Description')
    schedule_date = fields.Date('Fecha vencimiento')
    

    #@api.onchange('product_id')
    #def onchange_product_id(self):
    #    if self.product_id:
    #        name = self.product_id.name
    #        code = self.product_id.code
    #        sup_info_id = self.env['product.supplierinfo'].search([
    #            '|', ('product_id', '=', self.product_id.id),
    #            ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
    #            ('name', '=', self.wiz_id.supplier_id.id)])
    #        if sup_info_id:
    #            p_code = sup_info_id[0].product_code
    #            p_name = sup_info_id[0].product_name
    #            name = '[%s] %s' % (p_code if p_code else code,
    #                                p_name if p_name else name)
    #        else:
    #            if code:
    #                name = '[%s] %s' % (code, name)
    #        if self.product_id.description_purchase:
    #            name += '\n' + self.product_id.description_purchase
    #        self.product_uom_id = self.product_id.uom_id.id
    #        self.product_qty = 1.0
    #        self.name = name
