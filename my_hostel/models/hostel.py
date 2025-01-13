from odoo import fields, models, api

class Hostel(models.Model):
	_name = 'hostel.hostel'
	# _rec_name = "my_hostel_hostel" - renombrar el registro
	# _inherit = "res.partner" [act1]
	# _name = 'model_hostel_hostel' - id externo
	_order = "id asc ,name" #orden por i y nombre, el id sera de manera ascendente
	_description = 'Information about hostel'
	_rec_name = 'hostel_code' 
	# _rec_names_search = ['name', 'code','street']
	"""[act2]"""
	# my_hostel_hostel = fields.Char(string='Hotel Name', required=True)
	name = fields.Char(string='Hotel Name', required=True)
	hostel_code = fields.Char(string='Code',required=True)
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	state_id = fields.Many2one('res.country.state',string="State")
	zip = fields.Char('Zip', change_default=True)
	city = fields.Char('City')
	state_id = fields.Many2one("res.country.state", string='State')
	country_id = fields.Many2one('res.country', string='Country')
	phone = fields.Char('Phone',required=True)
	mobile = fields.Char('Mobile',required=True)
	email = fields.Char('Email')
	#Este campo es de tipo entero, nos pide en total de pisos del hotel
	hostel_floors = fields.Integer(string="Total Floors")
	#Este campo almacena una imagen al entrar al formulario
	image = fields.Binary('Hostel Image')
	"""
		este campo es un check en donde estara activado por defecto
		y el help nos dice para que sirve el check 
	"""
	active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
	"""
		este es un campo, de seleccion que tiene varios parametros
		el primero es una lista
		el segundo es el tipo de campo,
		el tercero el icono de ayuda donde nos especifica que informacion se ingresa
		el cuarto parametro es un campo requerido para poder enviar el form
		el quinto es un texto que aparece por defecto en la seleccion 	
	"""
	
	type = fields.Selection([
        ("male", "Boys"), 
        ("female", "Girls"), 
        ("common", "Common")
    ], "Type", help="Type of Hostel", required=True, default="common")
	# un campo de texto donde pondremos otra informacion y un icono de ayuda que nos dice que tipo de informacion podemos ingresas
	other_info = fields.Text("Other Information", help="Enter more information")
	#una descripcion
	description = fields.Html('Description')
	# Creamos un campo flotante, con digitos que pueden tener ciertos numeros de digitos, 14 digitos hasta la izquierda, y 4 hacia la derecha 
	# hostel_rating = fields.Float('Hostel Average Rating', digits=(14, 4)) Metodo 1
	hostel_rating = fields.Float('Hostel Average Rating', digits='Rating Value' ) # Metodo 2
	
	ref_doc_id = fields.Reference(selection='_referencable_models',string='Reference document')
	
	is_public = fields.Boolean(string="Public",groups="my_hostel.group_hostel_manager")

	notes = fields.Text(string="Some Text",groups="my_hostel.group_hostel_manager")
	# category_id = fields.Many2one('hostel.category')
	@api.depends('hostel_code')
	def _compute_display_name(self):
		for record in self:
			name = record.name
			if record.hostel_code:#si existe, hostel_code, entonces
				#guarda en la variable name el texto que tendra como balor nombre del registro
				#y el valor de Hostel_code
				name = f'{name} ({record.hostel_code})' 
			record.display_name = name

	@api.model
	def _referencable_models(self):
		modelos = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
		return [(x.name, x.model) for x in modelos]