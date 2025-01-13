from odoo import models, fields

class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the hostel amenity provided"
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Activate or deactivate this amenity"
    )

