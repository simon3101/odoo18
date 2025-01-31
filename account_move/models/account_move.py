from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_tax_base = fields.Monetary(
            string='Amount tax base', 
            required=True, 
            readonly=True,
            stored=True,
            compute='_compute_amount_own')

    @api.depends(
        'line_ids',
        )
    def _compute_amount_own(self):
        for move in self:
            # me esta recorriendo las facturas
            move.amount_tax_base = 0.0
            line_taxes = move.line_ids.filtered(lambda t: t.tax_ids.amount > 0)
            for line in line_taxes: 
                # me esta recorriendo las lineas de la factura
                print('taxes',line.price_subtotal)
                move.amount_tax_base += line.price_subtotal
                # print("move",move.line_ids.tax_ids.amount)

    def _compute_tax_totals(self):
        super()._compute_tax_totals(self.amount_tax_base)