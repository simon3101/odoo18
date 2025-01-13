import logging

from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
    # _rec_names_search = ["id","name","roomNo"]

    user_id = fields.Many2one('res.users', string='User')
    remarks = fields.Char('Remarks')
    #Aca la relacion es de, muchas habitaciones que tiene un hotel (many), hay solo un hotel, por lo tanto el campo es Many2one
    hostel_id = fields.Many2one(
        'hostel.hostel',#Nombre del modelo, en este caso del hostel hostel
        string='Hostel',#Nombre en la vista del modelo
        help='Name of my the hostel '
        )

    name = fields.Char("Room Name",required=True)
    roomNo = fields.Integer("Room No")
    floorNo = fields.Integer("Floor No")
    
    currency_id = fields.Many2one('res.currency',string='Currency')
    
    rent_amount = fields.Monetary('Rent Amount', help="Enter a rent amount per month")
    student_ids = fields.One2many(
                                "hostel.student",
                                "room_id", 
                                string="Students", 
                                help="Enter students"
                                )
    hostel_amenities_ids = fields.Many2many(
        "hostel.amenities",
        "hostel_room_amenities_rel", 
        "room_id", 
        "amenitiy_id",
        string="Amenities", 
        domain="[('active', '=', True)]",
        help="Select hostel room amenities"
    )
    
    student_per_room = fields.Integer("Students per Room", help="Room student assignment")

    availability = fields.Float(compute="_compute_check_availability",store=True, string="Avalaibility",help="Avalaibility hostal's room")

    authored_book_ids = fields.Many2many("res.partner")

    state = fields.Selection([
        ('draft', 'No available'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        string='State',
        default='draft'
    )

    category_id = fields.Many2one('hostel.category')

    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')



    def find_room(self):
        print(self.category_id.name)
        domain = [
            '|',  
                '&',  
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

    def log_all_room_members(self):
        
        hostel_room_obj = self.env['hostel.room']
        all_members = hostel_room_obj.search([])
        print("TODOS LOS MIEMBROS:", all_members)
        return True

    def update_room_no(self):
        self.roomNo = self.id
    
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

            
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # nos ayudara a verificar si el estado existe
        allowed = [
            ('draft', 'available'),
            ('available', 'closed'),
            ('closed', 'draft')
        ]
        
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        # nos ayudara a cambiar el estado al que el usuario quiera
        for room in self:
            print(room)
            
            if room.is_allowed_transition(room.state, new_state): 
                room.state = new_state
            else:
                _logger.exception("No tienes permiso para crear un registro con algun valor en remarks")
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)

    def make_available(self):
        # nos ayudara para que cuando se presione el boton cambie de estado a available
        self.change_state('available')

    def make_closed(self):
        # nos ayudara para que cuando se presione el boton cambie el estado a closed
        self.change_state('closed')

    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.room_with_multiple_members(all_rooms)
        _logger.info('Filtered Rooms: %s', filtered_rooms)
    
    @api.model
    def room_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
            return False
        return all_rooms.filtered(predicate)

    def get_mapped_amenities(self):
        all_rooms = self.search([])
        mapped_amenties = all_rooms.get_amenities_names(all_rooms)
        _logger.info('Filtered Rooms : %s', mapped_amenties)
        _logger.warning('Filtered Rooms: %s',mapped_amenties)
        _logger.error('Filtered Rooms: %s',mapped_amenties)
        _logger.critical('Filtered Rooms: %s',mapped_amenties)
    
    @api.model
    def get_amenities_names(self,all_rooms):
        print("Modelo hostel.room",self) 
        print("id del room donde estoy llamando a la accion ",all_rooms)
        return all_rooms.mapped('hostel_amenities_ids.name')

    def sorted_list(self):
        all_rooms = self.search([])
        sorted_recs = all_rooms.sort_records(all_rooms)
        _logger.info('Filtered Rooms: %s', sorted_recs)
    
    @api.model
    def sort_records(self,rooms):
        return rooms.sorted('rent_amount')

    @api.model
    def create(self, values):
        _logger.info('Filtered Rooms: %s', values)#1
        _logger.info('Filtered Rooms: %s', self)#hostel.room()
        _logger.info('Filtered Rooms: %s',self.env.user)#res.users(2,)
        user = self.env.user
        if not user.has_groups("my_hostel.group_hostel_manager"):
            values.get('remarks')
            if values.get('remarks'):
                raise UserError(
                    'No tienes permiso para crear un registro con algun valor en "remarks".'
                )
        return super(HostelRoom, self).create(values)

    def write(self, values):
        _logger.info('Filtered Rooms - 1: %s', values)
        _logger.info('Filtered Rooms - 2: %s', self)
        user= self.env.user
        _logger.info('Filtered Rooms - 3: %s', user.has_groups('my_hostel.group_hostel_manager'))
        if not user.has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'No tienes permiso para modificar "remarks".'
                )
        return super(HostelRoom, self).write(values)

    def _compute_display_name(self):
        for room in self:
            amenities = room.hostel_amenities_ids.mapped('name')
            name = '%s %s (%s)' % (room.id,room.name, ', '.join(amenities))  
            room.display_name = f'{name}'
        return

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|', '|',
                        ('name', operator, name),
                        ('roomNo', operator, name),
                        ('hostel_amenities_ids.name', operator, name)
                    ]
        else:
            raise UserError(
                    'No se esta haciendo la busqueda como deberia".'
                )
        return super(HostelRoom, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
    
    @api.model
    def _get_average_cost(self,room):

        grouped_result = self.read_group(
            [('rent_amount', "!=", False)],  
            ['category_id', 'rent_amount:avg'],  
            ['category_id']  
        )
        _logger.info('Filtered Rooms - 1: %s', grouped_result)
        _logger.info('Filtered Rooms - 1: %s', room)
        for g in grouped_result:
            print(g)
        return grouped_result

    def get_average(self):
        result = self._get_average_cost(self)
    
    @api.model
    def _update_room_price(self):
        all_rooms = self.search([])
        for room in all_rooms:
            room.rent_amount = room.rent_amount + 10

    # Cap 8.2
    def action_remove_room_members(self):
        for student in self.student_ids:
            # is_hostel_room = true es el contexto que tendran los registros del hostel_student para poder llamar al metodo action_remove_room
            student.with_context(is_hostel_room=True).action_remove_room()

    # Cap 8.3
    def action_category_with_amount(self):
        self.env.cr.execute(""" 
            SELECT
                name,
                rent_amount
            FROM
                hostel_room
            WHERE
                hostel_room.name = %(room_name)s
        """, {'room_name': self.name})
        result = self.env.cr.fetchall()
        _logger.warning("Hostel Room With Amount: %s", result)

    