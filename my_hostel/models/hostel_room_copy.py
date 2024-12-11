from odoo import models, fields,api

class HostelRoomCopy(models.Model):
    _name = "hostel.room.copy"
    _inherit = "hostel.room"
    _description = "Hostel Room Information Copy"

    hostel_amenities_ids = fields.Many2many(
        'hostel.amenities',
        'hostel_room_amenities_rel_copy',  # Nombre de la tabla intermedia
        'room_id',  # Columna para este modelo
        'amenity_id',  # Columna para el otro modelo
        string='Hostel Amenities'
    )