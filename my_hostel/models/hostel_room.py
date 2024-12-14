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
    
    remarks = fields.Char('Remarks')
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

    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')
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
        hostel_room_obj = self.env['hostel.room']
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
        # print(old_state,new_state)
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        # con esta funcion pasamos de un estado a otro
        for room in self:
            print(room)
            # esto nos dice, aca estamos en el registro con id = 3
            if room.is_allowed_transition(room.state, new_state): # si la condicion existe entonces sigue
                # print(room.state) # draft
                room.state = new_state # este sera el nuevo estado por defecto
                # print(room.state) # available o clased (dependiendo de lo que elija el usuario)
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
        # print("All rooms, es igual a: " ,all_rooms) =. lista completa de registros del modelo
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

    def get_mapped_amenities(self):
        all_rooms = self.search([])# esto traera una lista de registros
        mapped_amenties = all_rooms.get_amenities_names(all_rooms)
        _logger.info('Filtered Rooms: %s', mapped_amenties)
    
    @api.model
    def get_amenities_names(self,all_rooms):
        print("Modelo hostel.room",self) # => hostel.room()
        print("id del room donde estoy llamando a la accion ",all_rooms) # => [5]
        # print("Este es el room",room) # => error de argumentos pasados, por tanto room no puede ir
        # print("Este es el mapped de amenities id usando el modelo instanciado pero si registros asociados: ",self.mapped('hostel_amenities_ids')) # => []
        return all_rooms.mapped('hostel_amenities_ids.name')

    def sorted_list(self):
        all_rooms = self.search([])
        sorted_recs = all_rooms.sort_records(all_rooms)
        _logger.info('Filtered Rooms: %s', sorted_recs)
    
    @api.model
    def sort_records(self,rooms):
        # print(rooms.student_ids.gender)
        return rooms.sorted('rent_amount')

    @api.model
    def create(self, values):
        # Este metodo extendido solo funcionara para los admin, debido a que el grupo user no tiene permiso para crear
        _logger.info('Filtered Rooms: %s', values)#1
        _logger.info('Filtered Rooms: %s', self)#hostel.room()
        _logger.info('Filtered Rooms: %s',self.env.user)#res.users(2,)
        user = self.env.user
        # Aca tambien podria funcionar un if (condicion) == False
        if not user.has_groups("my_hostel.group_hostel_manager"):
            values.get('remarks')
            if values.get('remarks'):
                raise UserError(
                    'No tienes permiso para crear un registro con algun valor en "remarks".'
                )
        return super(HostelRoom, self).create(values)

    def write(self, values):
        _logger.info('Filtered Rooms - 1: %s', values) #valor de remarks
        _logger.info('Filtered Rooms - 2: %s', self)# instancia del objecto con el id del registro en el que estamos, o recordset
        user= self.env.user
        _logger.info('Filtered Rooms - 3: %s', user.has_groups('my_hostel.group_hostel_manager')) #False
        # Aca tambien podria funcionar un if (condicion) == False
        if not user.has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'No tienes permiso para modificar "remarks".'
                )
        return super(HostelRoom, self).write(values)

    # como este metodo ya no se usa en la 18, el return result no, arroja nada
    # por tanto estamos es creando un metodo name_get, mas no estamos sobreescribiendolo, como nos aparece en el libro
    
    def name_get(self):
        result = []
        # print(self.name_get())
        self.display_name
        for room in self:
            members = room.hostel_amenities_ids.mapped('name')
            name = '%s (%s)' % (room.name, ', '.join(members))
            result.append((room.id, name))
            print(self.display_name)
        _logger.info('Filtered Rooms: %s',result)#id y name y amenities
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        # Creamos una copia de los argumentos para evitar modificar los originales
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            # el name search necesita una dominio para funcionar, por tanto le agregamos este
            args += ['|', '|',
                        ('name', operator, name),
                        ('roomNo', operator, name),
                        ('hostel_amenities_ids.name', operator, name)
                    ]
        
        return super(HostelRoom, self)._name_search(
            name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
