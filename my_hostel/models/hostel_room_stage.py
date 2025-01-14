from odoo import models, fields


class HostelRoomStage(models.Model):
    _name = 'hostel.room.stage'
    _order = 'sequence,name'
    name = fields.Char("Name")
    sequence = fields.Integer("Sequence")
    fold = fields.Boolean("Fold?")
