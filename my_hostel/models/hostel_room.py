import logging

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import timedelta
# cap 5.2
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

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
    # Cap 4
    state = fields.Selection([
        ('draft', 'No available'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        string='State', 
        default='draft'
    )

    category_id = fields.Many2one('hostel.category')
    # cap 5.6
    def find_room(self):
        print(self.category_id.name)
        domain = [
            '|',  # Operador lógico OR
                '&',  # Operador lógico AND
                    ('name', 'ilike', 'Room Name'),
                    ('category_id', "ilike", 'Child category 1'),
                '&',
                    ('name', 'ilike', 'Second Room Name 2'),
                    ('category_id.name', "ilike", 'Child category 2'),
        ]

        rooms = self.search(domain)
        print("Habitaciones encontradas:", rooms)
        return rooms

    def combining_records(self):
        recordset_1 = self.search([("name","ilike",'Room Name')])
        recordset_2 = self.search([("rent_amount",">=",100)])
        result = recordset_1 + recordset_2
        return print(result)
    # cap 5.3
    def log_all_room_members(self):
        # Este es un conjunto de registros vacío del modelo hostel.room.member
        hostel_room_obj = self.env['hostel.room.members']
        all_members = hostel_room_obj.search([])
        print("TODOS LOS MIEMBROS:", all_members)
        return True

    # cap 5.5 
    def update_room_no(self):
        self.ensure_one()  # Asegura que solo se esté trabajando con un registro.
        self.roomNo = "002"
    
    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Método para comprobar la disponibilidad de la habitación"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Restricción para monto de alquiler negativo"""
        if self.rent_amount < 0:
            raise ValidationError(("the month rent amount can't be negative!"))

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
    # Cap 5
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('draft', 'available'),
            ('available', 'closed'),
            ('closed', 'draft')
        ]
        print(old_state,new_state)
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        # con esta funcion pasamos de un estado a otro
        for room in self:
            print(room)
            # esto nos dice, aca estamos en el registro con id = 3
            if room.is_allowed_transition(room.state, new_state): # si la condicion existe entonces sigue
                print(room.state) # draft
                room.state = new_state # este sera el nuevo estado por defecto
                print(room.state) # available o clased (dependiendo de lo que elija el usuario)
            else:
                # room.is_allowed_transition(room.state, new_state) si este es false arrojara este error
                # Cap 5.2
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')
    # cap 5.8
    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.room_with_multiple_members(all_rooms)
        _logger.info('Filtered Rooms: %s', filtered_rooms)
        # print(filtered_rooms)
    
    @api.model
    def room_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
            return False
        return all_rooms.filtered(predicate)

    # def all_rooms_with_category(self):
    #     all_rooms = self.search([])
    #     # este solo me retornara todos los
    #     return print (all_rooms.filtered('category_id'))
    
    # def get_amenities_names(self):
    #     return print(self.mapped('hostel_amenities_ids.name'))

    @api.model
    def get_amenities_names(self,all_rooms):
        # print("ola mundo")
        # print(type(rooms))
        # print(type(self))
        # print(self)
        # print(self)
        return all_rooms.mapped('name')