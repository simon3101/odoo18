from odoo import fields, models
from odoo import tools
class HostelRoomAvalability(models.Model):
    _name = 'hostel.room.availability'
    _description = 'Avalabity of the rooms'
    _auto = False

    room_id = fields.Many2one('hostel.room', 'Room', readonly=True)
    student_per_room = fields.Integer(string="Student Per Room", readonly=True)
    availability = fields.Integer(string="Availability", readonly=True)
    amount = fields.Integer(string="Amount", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
        CREATE OR REPLACE VIEW hostel_room_availability AS (
            SELECT
                min(h_room.id) as id,
                h_room.id as room_id,
                h_room.student_per_room as student_per_room,
                h_room.availability as availability,
                h_room.rent_amount as amount
            FROM
                hostel_room AS h_room
            GROUP BY h_room.id
        );
        """
        self.env.cr.execute(query)



