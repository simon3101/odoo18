import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class HostelCategory(models.Model):
    _name = "hostel.category"
    _description = "Hostel Category"
    _parent_store = True #
    _parent_name = "parent_id" # optional if field is 'parent_id'
    
    name = fields.Char(string="Category Name", required=True, help="Name of the category")
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        comodel_name="hostel.category",
        string="Parent Category",
        ondelete="restrict",# Si se intenta borrar la referencia dara un error si hay una creada
        index=True,# esto es para ser indexado en la base de datos, por defecto no lo esta, si lo esta es mas rapido consultar
        help="Parent category in the hierarchy",
    )
    parent_path = fields.Char(index=True,readonly=True)

    child_ids = fields.One2many(
        comodel_name="hostel.category",
        inverse_name="parent_id",
        string="Child Categories",
        help="Subcategories of this category"
    )
    create_category_id = fields.Many2one('hostel.category')

    state = fields.Selection([
        ('draft', 'No available'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        string='State',
        default='draft'
    )

    date_assign = fields.Date(string='Assignment Date')
    date_end = fields.Datetime(string='End Date')


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
    
    # Método para generar categorías ficticias
    def create_categories(self):
        # Diccionario con los valores de la primera subcategoría
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        # Diccionario con los valores de la segunda subcategoría
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        # Diccionario con los valores de la categoría principal
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        record = self.create(parent_category_val)
        return record

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    def log_parent(self):
        return print(self.parent_path)
