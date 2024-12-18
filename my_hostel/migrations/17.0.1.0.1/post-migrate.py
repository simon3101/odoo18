from odoo import fields
from datetime import date

def migrate(cr, version):
    cr.execute('SELECT id, allocation_date_char FROM hostel_room')
    for record_id, old_date in cr.fetchall():
        new_date = None
        try:
            # Intenta convertir el valor al formato de fecha de Odoo
            new_date = fields.Date.to_date(old_date)
        except ValueError:
            # Si el valor es un año (por ejemplo, "2023")
            if len(old_date) == 4 and old_date.isdigit():
                new_date = date(int(old_date), 1, 1)
        if new_date:
            cr.execute('UPDATE hostel_room SET allocation_date=%s WHERE id=%s', (new_date, record_id))
