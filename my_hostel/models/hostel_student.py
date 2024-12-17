from odoo import models, fields


class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = "Student model"
    _inherits = {'res.partner': 'partner_id'}
# name = fields.Char(
    #     string="Student Name",
    #     help="Name of the student"
    # )
    
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other")
        ],
        string="Gender",
        help="Student's gender"
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Activate or deactivate the hostel record"
    )
    # Esta es la relacion que pueden tener muchos estudiantes a una habitacion
    #Aqui se seleccionara una habitacion
    room_id = fields.Many2one(
        "hostel.room",#nombre del comodelo
        string="Room",#string del campo
        required=False,
        help="Select the hostel room"#ayuda para el campo
    )

    hostel_id = fields.Many2one(
        "hostel.hostel", 
        string="Hostal", 
        related='room_id.hostel_id'
    )

    partner_id = fields.Many2one('res.partner',string="Partner",ondelete='cascade', required=True )