# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.fields import Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            account = self.env['customer.account'].search([('partner_id', '=', self.partner_id.id)], limit=1)
            if account:
                self.analytic_account_id = account.analytic_account_id.id


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            offer = self.env['seasonal.offers'].search([('product_id', '=', self.product_id.product_tmpl_id.id)], limit=1)
            if offer:
                self.analytic_distribution = {offer.analytic_account_id.id: 100}



    """ If not choose other analytic distribution you can choose  
        given below function """

    # def _prepare_invoice_line(self, **optional_values):
    #
    #     offer = self.env['seasonal.offers'].search([('product_id', '=', self.product_id.product_tmpl_id.id)], limit=1)
    #     account = self.env['customer.account'].search([('partner_id', '=', self.order_id.partner_id.id)], limit=1)
    #
    #     """Prepare the values to create the new invoice line for a sales order line.
    #
    #     :param optional_values: any parameter that should be added to the returned invoice line
    #     :rtype: dict
    #     """
    #     self.ensure_one()
    #     res = {
    #         'display_type': self.display_type or 'product',
    #         'sequence': self.sequence,
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'product_uom_id': self.product_uom.id,
    #         'quantity': self.qty_to_invoice,
    #         'discount': self.discount,
    #         'price_unit': self.price_unit,
    #         'tax_ids': [Command.set(self.tax_id.ids)],
    #         'sale_line_ids': [Command.link(self.id)],
    #         'is_downpayment': self.is_downpayment,
    #     }
    #
    #
    # ############## ANALYTIC ACCOUNT INTEGRATION START ###################
    #
    #     if account and offer:
    #         res['analytic_distribution'] = {str(offer.analytic_account_id.id): 100,str(account.analytic_account_id.id): 100}
    #     elif offer:
    #         res['analytic_distribution'] = {str(offer.analytic_account_id.id): 100}
    #     elif account:
    #         res['analytic_distribution'] = {str(account.analytic_account_id.id): 100}
    #
    # ############## ANALYTIC ACCOUNT INTEGRATION END #####################
    #
    #     if optional_values:
    #         res.update(optional_values)
    #     if self.display_type:
    #         res['account_id'] = False
    #     return res

