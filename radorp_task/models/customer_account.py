# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CustomerAccount(models.Model):
    _name = 'customer.account'
    _description = 'Customer Account'

    name = fields.Char(string='Account Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)

    _sql_constraints = [('partner_unique', 'unique(partner_id)', 'Each customer can have only one account associated with them')]

    # Analytic account creation based on customer account
    @api.model
    def create(self, vals):
        account = super(CustomerAccount, self).create(vals)
        analytic_account = self.env['account.analytic.account'].create({
            'name': f"Customer Account: {account.name}",
            'plan_id': self.env.ref('radorp_task.customer_account_plan').id,
        })
        account.analytic_account_id = analytic_account.id
        return account
