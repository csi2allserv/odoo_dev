# -*- coding: utf-8 -*-
from odoo import http

# class Ejempp(http.Controller):
#     @http.route('/ejempp/ejempp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ejempp/ejempp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ejempp.listing', {
#             'root': '/ejempp/ejempp',
#             'objects': http.request.env['ejempp.ejempp'].search([]),
#         })

#     @http.route('/ejempp/ejempp/objects/<model("ejempp.ejempp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ejempp.object', {
#             'object': obj
#         })