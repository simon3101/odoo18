from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    group_hostel_user = fields.Boolean(
        string="Hostel User",
        implied_group='my_hostel.group_hostel_user',
    )
    group_start_date = fields.Boolean( "Manage Start Date",  
        group='base.group_user',  
        implied_group='my_hostel.group_start_date',  
    )

    module_note = fields.Boolean("Install Note Module") 