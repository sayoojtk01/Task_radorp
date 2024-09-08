# -*- coding: utf-8 -*-
{
    "name": "Task Radorp",
    "summary": """ Interview task """,
    "category": "Accounting",
    "version": "16.0.1.0.0",
    "author": "SAYOOJ T K",
    "license": "LGPL-3",
    "description": """  This module aims to extracting account move lines by time 
                        period and Creation of seasonal offers and customer 
                        accounts models with analytic account integration  """,
    "depends": ['base', 'account','sale_management', 'report_xlsx'],
    "data": [
        'security/ir.model.access.csv',
        'data/analytic_plans.xml',
        'views/seasonal_offers.xml',
        'views/customer_account.xml',
        'reports/extract_account_move_lines.xml',
        'reports/report_action.xml',
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
