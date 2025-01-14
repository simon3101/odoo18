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
	hostel_floors = fields.Integer(string="Total Floors")
	image = fields.Binary('Hostel Image')
	active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
	type = fields.Selection([
        ("male", "Boys"), 
        ("female", "Girls"), 
        ("common", "Common")
    ], "Type", help="Type of Hostel", required=True, default="common")
	other_info = fields.Text("Other Information", help="Enter more information")
	description = fields.Html('Description')
	# hostel_rating = fields.Float('Hostel Average Rating', digits=(14, 4)) Metodo 1
	hostel_rating = fields.Float('Hostel Average Rating', digits='Rating Value' ) # Metodo 2
	ref_doc_id = fields.Reference(selection='_referencable_models',string='Reference document')
	# Fields with groups
	is_public = fields.Boolean(string="Public",groups="my_hostel.group_hostel_manager")
	notes = fields.Text(string="Some Text",groups="my_hostel.group_hostel_manager")
	date_start = fields.Date(string='Init date', groups='my_hostel.group_start_date',)
	details_added = fields.Text( string="Details", groups='my_hostel.group_hostel_manager')
	# category_id = fields.Many2one('hostel.category')
	
	def add_details(self):
		self.ensure_one()
		message = "Details are (added by: %s)" % self.env.user.name
		self.sudo().write({
			'details_added': message
		})

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