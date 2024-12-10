from odoo import fields, models, api

class HostelRoomMembers(models.Model):
    _name = 'hostel.room.members'
    _description = 'Members of the hostel'

    name = fields.Char(string='Name of the member')

