from odoo import fields, models

class ModelInline(models.Model):
    _name = 'model.inline'
    _description = 'Model Inline'


    name = fields.Char('inline name',required=True)
    description = fields.Char(string="Description")
    line_ids = fields.One2many("model.inline.test", "model_id",string="tags")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

class  ModelTestInline(models.Model):
    _name = 'model.inline.test'
    _description = 'Model Inline'

    model_id = fields.Many2one("model.inline",string="Model", readonly=True)
    name = fields.Char('name',required=True)
    color = fields.Integer(string="Color",readonly=True)