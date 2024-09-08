# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SeasonalOffers(models.Model):
    _name = 'seasonal.offers'
    _description = 'Seasonal Offers'

    name = fields.Char(string='Offer Name', required=True)
    product_id = fields.Many2one('product.template', string='Product', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)

    _sql_constraints = [('product_unique', 'unique(product_id)', 'Each product can only be associated with one seasonal offer.')]


    # Analytic account creation based on offer
    @api.model
    def create(self, vals):
        offer = super(SeasonalOffers, self).create(vals)
        analytic_account = self.env['account.analytic.account'].create({
            'name': f"Seasonal Offer: {offer.name}",
            'plan_id': self.env.ref('radorp_task.seasonal_offers_plan').id,
        })
        offer.analytic_account_id = analytic_account.id
        return offer
