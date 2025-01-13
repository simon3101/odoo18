from odoo import fields, models

class View_model(models.Model):
    _name = "view.model"
    _description = "Principal model view"

    name = fields.Char(string="Name", required=True)