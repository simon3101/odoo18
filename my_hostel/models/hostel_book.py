from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = "res.partner"
    is_hostel_rector = fields.Boolean("Rector de Hostel",help="Activar si la siguiente persona es rector de hostel")
    
    #Aca estamos asignando muchos libros a muchas habitaciones
    assign_room_ids = fields.Many2many('library.book', string='Libros Autorizados')
    #Aca calculamos con el meto _compute_count_room, la cantidad de libros asignado a la sala
    count_assign_room = fields.Integer('Número de Libros Autorizados', compute="_compute_count_room")

    @api.depends('assign_room_ids')
    def _compute_count_room(self):
        for socio in self:
            #aca me esta diciendo, cuantos libros tengo en la sala 'x'
            socio.count_assign_room = len(socio.assign_room_ids)