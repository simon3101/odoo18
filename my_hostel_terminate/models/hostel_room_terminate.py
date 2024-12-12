import logging
from odoo import api,models, fields
from datetime import timedelta

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):
    _inherit = 'hostel.room'

    date_terminate = fields.Date('Date of Termination')

    def make_closed(self):
        day_to_allocate = self.category_id.max_allow_days or 10
        self.date_terminate = fields.Date.today() + timedelta(days=day_to_allocate)
        # print("fields.Date.today()", fields.Date.today())
        # print(day_to_allocate)
        # print("timedelta: ",timedelta(days=day_to_allocate))
        # # print(fields.Date.today() + timedelta(days=day_to_allocate))
        return super(HostelRoom, self).make_closed()
    
    def make_available(self):
        self.date_terminate = False
        return super(HostelRoom, self).make_available()# con esto referenciamos al boton make_available ya creado


class RoomCategory(models.Model):
    _inherit = 'hostel.category'

    max_allow_days = fields.Integer(
        'Maximum allowed days',
        help="Maximum number of days a room can be borrowed",
        default=365
    )
