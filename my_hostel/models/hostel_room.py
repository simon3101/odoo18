from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class HostelRoom(models.Model):

    _name = 'hostel.room'
    _description = 'Hostel room model'
    #Esto que sigue son validades A nivel de SQL que puede tomar el programa
    _sql_constraints = [("room_no_unique", "unique(room_no)", "Room number must beunique!")]
    #("name", "Codigo sql", "Mensaje que mostrara")
    _inherit = ['base.archive']
    

    #Aca la relacion es de, muchas habitaciones que tiene un hotel (many), hay solo un hotel, por lo tanto el campo es Many2one
    hostel_id = fields.Many2one(
        'hostel.hostel',#Nombre del modelo, en este caso del hostel hostel
        string='Hostel',#Nombre en la vista del modelo
        help='Name of the hostell'
        )

    name = fields.Char("Room Name",required=True)
    roomNo = fields.Integer("Room No",required=True)
    floorNo = fields.Integer("Floor No",required=True)
    #Esto nos dice, crea el campo, en el registro, con la relacion de muchos a uno
    #el res.currency es un modelo de odoo, donde se encuentran las divisas almacenadas por odoo
    currency_id = fields.Many2one('res.currency',string='Currency', required=True)
    #Este sera un campo, donde tendra como valor la cantidad monetaria segun la denominacion
    rent_amount = fields.Monetary('Rent Amount', help="Enter a rent amount per month")
    student_ids = fields.One2many(
                                "hostel.student",#Nombre del comodelo que se relacion
                                "room_id", #variable del comodelo a la hacemos referencia
                                string="Students", #texto del campo
                                help="Enter students"# ayuda en el campo
                                )
    hostel_amenities_ids = fields.Many2many(
        "hostel.amenities",#comodelo relacionado, en este caso amenities
        "hostel_room_amenities_rel", #nombre de la tabla relacionada, si no esta creada, se crea una
        "room_id", #campo many2one del modelo student
        "amenitiy_id", #campo many2one del modelo Amenity que se relaciona con el campo many2one del modelo Student #si no existe este nombre se crea por defecto,  #por lo general estos son parametros opcionales
        string="Amenities", 
        domain="[('active', '=', True)]",
        help="Select hostel room amenities"
    )

    
    #campo que tendra el numero de estudiantes que cabran por habitacion
    student_per_room = fields.Integer("Students per Room", required=True, help="Room student assignment")
    #este sera el campo calculado
    availability = fields.Float(compute="_compute_check_availability",store=True, string="Avalaibility",help="Avalaibility hostal's room")

    #sera un campo donde agreguemos una fecha de admision
    admission_date = fields.Date("Admission Date", help="Admission Hostal's Date",default=fields.Datetime.today)
    discharge_date = fields.Date("Up date", help="Up student's Date")
    duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration",help="insert duration")
    
    authored_book_ids = fields.Many2many("res.partner")

    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Método para comprobar la disponibilidad de la habitación"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Restricción para monto de alquiler negativo"""
        if self.rent_amount < 0:
            raise ValidationError(("¡El monto de alquiler mensual no debe ser negativo!"))

#este decorador calculara la duracion del estudiante, en base a si fecha de admision y la fecha de salida
    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Método para calcular la duración"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days

    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')        