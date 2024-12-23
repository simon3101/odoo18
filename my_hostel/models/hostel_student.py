from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _
# cap 8.6
from odoo.tests.common import Form
import logging

_logger = logging.getLogger(__name__)

class HostelStudent(models.Model):
    _name = "hostel.student"    
    _description = "Student model"
    # _inherits = {'res.partner': 'partner_id'}
    name = fields.Char(
            string="Student Name",
            help="Name of the student"
        )
    
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other")
        ],
        string="Gender",
        help="Student's gender"
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Activate or deactivate the hostel record"
    )
    room_id = fields.Many2one(
        "hostel.room",#nombre del comodelo
        string="Room",#string del campo
        required=False,
        help="Select the hostel room"#ayuda para el campo
    )

    hostel_id = fields.Many2one(
        "hostel.hostel", 
        string="Hostal", 
        related='room_id.hostel_id'
    )

    # partner_id = fields.Many2one('res.partner',string="Partner", ondelete='cascade',default=name)
    # cap 8
    status = fields.Selection(  
                                [
                                    ("draft", "Draft"),  
                                    ("reservation", "Reservation"), 
                                    ("pending", "Pending"),  
                                    ("paid", "Paid"),
                                    ("discharge", "Discharge"), 
                                    ("cancel","Cancel")
                                ],  
                                string="Status", 
                                copy=False, 
                                default="draft",  
                                help="State of the student hostel"
                            )

    admission_date = fields.Date("Admission Date", help="Admission Hostal's Date",default=fields.Datetime.today)
    discharge_date = fields.Date("Up date", help="Up student's Date")
    duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration",help="insert duration")
    duration_month = fields.Integer("Duration in month",compute="onchange_duration",inverse="_inverse_duration",help="insert duration")

    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Método para calcular la duración"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days

    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ("draft", "reservation"),  
            ("reservation", "pending"), 
            ("pending", "paid"),  
            ("paid", "discharge"),
            ("discharge", "cancel"), 
            ("cancel","draft"),
        ]
        print((old_state, new_state) in allowed)
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        
        for room in self:
            print(room.status)
            print(new_state)
            print(room.is_allowed_transition(room.status, new_state))
            if room.is_allowed_transition(room.status, new_state): 
                room.status = new_state
            else:
                # _logger.exception("No tienes permiso para crear un registro con algun valor en remarks")
                msg = _('Moving from %s to %s is not allowed') % (room.status, new_state)
                raise UserError(msg)

    def make_reservation(self):
        self.change_state('reservation')

    def make_pending(self):
        self.change_state('pending')

    def make_paid(self):
        self.change_state('paid')

    def make_discharge(self):
        self.change_state('discharge')

    def make_cancel(self):
        self.change_state('cancel')
    # 8.1    # 
    def action_assign_room(self):
        self.ensure_one()  
        if self.status != "paid":  
            raise UserError(_("You can't assign a room if it's not paid."))
        room_as_superuser = self.env['hostel.room'].sudo()  
        room_rec = room_as_superuser.create({  
            "name": "Room A-103",  
            "roomNo": "103",  
            "floorNo": 1,  
            "category_id": self.env.ref("my_hostel.room_category_not_remove").id,  
            "hostel_id": self.hostel_id.id,
            'student_ids': [(1, 0, self.name)],  
        })  
        if room_rec:
            self.room_id = room_rec.id
    # cap 8.2
    def action_remove_room(self):  
        if self.env.context.get("is_hostel_room"):  
            self.room_id = False  
    # cap 8.5
    @api.depends('admission_date', 'discharge_date')
    def onchange_duration(self):
        # Aca recalculamos la duration pero en meses
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                print(rec.discharge_date.year)
                print(rec.admission_date.month)
                print(rec.discharge_date.year - rec.admission_date.year)
                print(rec.discharge_date.month - rec.admission_date.month)
                print(rec)
                rec.duration_month = (rec.discharge_date.year - rec.admission_date.year) * 12 + \
                                (rec.discharge_date.month - rec.admission_date.month)
    # cap 8.6
    def return_room(self):
        self.ensure_one()
        wizard = self.env['assign.room.student.wizard']
        _logger.info('Info about wizard: %s',wizard)
        with Form(wizard) as return_form:
            return_form.room_id = self.env.ref('my_hostel.hostel_room_1')
            _logger.info('Info about return_room: %s',return_form)
            record = return_form.save()
            record.with_context(active_id=self.id).add_room_in_student()
            _logger.info('Record: %s',record.search([]))
    # cap 8.4
    def add_room_in_student_wizard(self):
        self.ensure_one()
        return {
            'name': 'Assign Room',
            'type': 'ir.actions.act_window',
            'res_model': 'assign.room.student.wizard',
            'target':'new',
        }
