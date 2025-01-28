from . import models
from . import controllers
from . import wizards

# from odoo import api, SUPERUSER_ID

# def add_room_hook(cr, registry):
#     env = api.Environment(cr, SUPERUSER_ID, {})
#     room_data4 = {
#         'name': 'Room 4',
#         'roomNo': 104,
#         'floorNo': 1,
#         'student_per_room': 2,  # Ensure this field name is correct
#         'rent_amount': 500.0,
#         'availability': 2.0,
#         'hostel_id': env.ref('my_hostel.hostel_1').id,
#     }
#     room_data5 = {
#         'name': 'Room 5',
#         'roomNo': 105,
#         'floorNo': 1,
#         'student_per_room': 3,  # Ensure this field name is correct
#         'rent_amount': 600.0,
#         'availability': 3.0,
#         'hostel_id': env.ref('my_hostel.hostel_1').id,
#     }
#     env['hostel.room'].create([room_data4, room_data5])

# def pre_init_hook_hostel(env):
#     env['ir.model.data'].search([
#         ('model', 'like', 'hostel.hostel'),
#     ]).unlink()

# def uninstall_hook_user(env):
#     hostel = env['res.users'].search([])
#     hostel.write({'active': True})
