from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_tax_base = fields.Monetary(
            string='Amount tax base', 
            required=True, 
            readonly=True,
            stored=True,
            compute='_compute_amount_own')

    @api.depends('line_ids.tax_ids',
                'line_ids.price_subtotal')
    def _compute_amount_own(self):
        for move in self:
            # me esta recorriendo las facturas
            amount_tax_base = 0.0
            line_taxes = move.line_ids.filtered(lambda t: t.tax_ids.amount > 0)
            for line in line_taxes: 
                print('taxes',line.price_subtotal)
                amount_tax_base += line.price_subtotal
            # actualizamos el campo en la base de datos al terminar el bucle for
            move.amount_tax_base += amount_tax_base

    
    def _compute_tax_totals(self):
        # Llamamos al super para mantener la lógica original
        super()._compute_tax_totals()
        for move in self:
            if move.tax_totals:
                # Agregamos nuestro nuevo valor al diccionario tax_totals
                move.tax_totals['amount_tax_base'] = move.amount_tax_base

        