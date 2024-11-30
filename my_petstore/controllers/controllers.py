# -*- coding: utf-8 -*-
# from odoo import http


# class MyPetstore(http.Controller):
#     @http.route('/my_petstore/my_petstore', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_petstore/my_petstore/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_petstore.listing', {
#             'root': '/my_petstore/my_petstore',
#             'objects': http.request.env['my_petstore.my_petstore'].search([]),
#         })

#     @http.route('/my_petstore/my_petstore/objects/<model("my_petstore.my_petstore"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_petstore.object', {
#             'object': obj
#         })

