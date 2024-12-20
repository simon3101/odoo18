from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.tools.translate import _

from datetime import *

# Cap 8.4
class AssignRoomStudentWizard(models.TransientModel):
    _name = 'assign.room.student.wizard'
    _description = 'Wizards that update some records of student'
    
    room_id = fields.Many2one("hostel.room", "Room", required=True)

    def add_room_in_student(self):
        self.ensure_one()
        hostel_room_student = self.env['hostel.student'].browse(self.env.context.get('active_id'))
        print(hostel_room_student)
        if hostel_room_student:
            hostel_room_student.update({
                'hostel_id': self.room_id.hostel_id.id,
                'room_id': self.room_id.id,
                'admission_date': datetime.today(),
            })
        # else:
        #     raise UserError(_('Context not found'))