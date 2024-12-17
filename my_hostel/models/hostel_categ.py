from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        help="Parent category in the hierarchy"
    )
    parent_path = fields.Char(index=True)

    child_ids = fields.One2many(
        comodel_name="hostel.category",
        inverse_name="parent_id",
        string="Child Categories",
        help="Subcategories of this category"
    )
    
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
