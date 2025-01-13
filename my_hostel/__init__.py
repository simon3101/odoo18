from . import models
from . import controllers
from . import wizards

from odoo import api, SUPERUSER_ID

def add_room_hook(env):
    # Enviroment toma como parametros basicos, curso de la base de datos, id del usuario, y un contexto vacio
    # env = api.Environment(cr, SUPERUSER_ID, {})
    room_data4 = {'name': 'Room 4', 'roomNo': '04','student_per_room0':'0'}
    room_data5 = {'name': 'Room 5', 'roomNo': '05','student_per_room0':'0'}
    env['hostel.room'].create([room_data4, room_data5])

def pre_init_hook_hostel(env):
    env['ir.model.data'].search([
        ('model', 'like', 'hostel.hostel'),
    ]).unlink()

def uninstall_hook_user(env):
    hostel = env['res.users'].search([])
    hostel.write({'active': True})
