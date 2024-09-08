# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
import base64
from io import BytesIO


class ExtractMoveLine(models.TransientModel):
    """Class defined for extract invoice lines wizard"""
    _name = 'extract.move.line'
    _description = "Extract Account Move Line Wizard Models"

    date_from = fields.Date(string="Date from",
                            help="Filter the report with the specified to date")
    date_to = fields.Date(string="Date to",
                          help="Filter the report with the specified from date")
    format = fields.Selection([('excel', ' Excel'), ('json', 'Json')], default='excel', string="Format",
                              help="Download the report with selected format", required=True)


    def action_generate_report(self):
        if self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')

        move_lines = self.env['account.move.line']
        domain = [('move_id.move_type', '=', 'out_invoice'), ('parent_state', '=', 'posted'),
                  ('product_id', '!=', None)]

        date_domain = []
        if self.date_from and self.date_to:
            date_domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        elif self.date_from:
            date_domain = [('date', '>=', self.date_from)]
        elif self.date_to:
            date_domain = [('date', '<=', self.date_to)]

        records = move_lines.search(domain + date_domain)
        movel_ine_list = []
        for rec in records:
            dic = {
               'invoice_number': rec.move_id.name,
               'invoice_date': str(rec.move_id.invoice_date),
               'item': rec.product_id.name,
               'quantity': rec.quantity,
               'uom': rec.product_uom_id.name,
               'price': rec.price_total,
            }
            movel_ine_list.append(dic)

        data = {
            'date_from': str(self.date_from) if self.date_from else '',
            'date_to': str(self.date_to) if self.date_to else '',
            'movel_ine_list': movel_ine_list
        }

        if self.format == 'json':
            return self._generate_json_report(data)
        else:
            return self.env.ref('radorp_task.acton_extract_move_line_report').report_action(self, data=data)


    def _generate_json_report(self, records):
        # Convert records to JSON format
        json_data = json.dumps(records, default=str)

        file_content = BytesIO(json_data.encode('utf-8'))
        file_content.seek(0)

        file_base64 = base64.b64encode(file_content.read()).decode('utf-8')

        attachment_name = 'account_move_line_report.json'
        attachment = self.env['ir.attachment'].create({
            'name': attachment_name,
            'type': 'binary',
            'datas': file_base64,
            'store_fname': attachment_name,
            'mimetype': 'application/json',
        })

        download_url = f'/web/content/{attachment.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'new',
        }



class ExtractMoveLineReportExcel(models.AbstractModel):
    """Class defined for create excel report for extract account move line """
    _name = 'report.radorp_task.extract_move_line_report_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        title_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14, 'bg_color': '#E0E0E0'})
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#E0E0E0'})
        header_format2 = workbook.add_format({'bold': True, 'align': 'left'})
        center_align = workbook.add_format({'align': 'center'})
        left_align = workbook.add_format({'align': 'left'})

        sheet = workbook.add_worksheet("Extract Account Move Lines Report")
        bold = workbook.add_format({'bold': True})

        sheet.merge_range('E1:I1', 'Extract Account Move Lines', title_format)

        sheet.merge_range('A2:B2', 'From Date:', header_format2)
        sheet.merge_range('C2:D2', str(data.get('date_from', '')), left_align)
        sheet.merge_range('A3:B3', 'To Date:', header_format2)
        sheet.merge_range('C3:D3', str(data.get('date_to', '')), left_align)

        sheet.merge_range('A5:B6', 'Invoice Number', header_format)
        sheet.merge_range('C5:D6', 'Invoice Date', header_format)
        sheet.merge_range('E5:F6', 'Item', header_format)
        sheet.merge_range('G5:H6', 'Quantity', header_format)
        sheet.merge_range('I5:J6', 'UOM', header_format)
        sheet.merge_range('K5:L6', ' Total Price', header_format)

        row = 6
        for employee_detail in data.get('movel_ine_list', []):
            sheet.merge_range(row, 0, row, 1, employee_detail.get('invoice_number', ''), center_align)
            sheet.merge_range(row, 2, row, 3, employee_detail.get('invoice_date', 0), center_align)
            sheet.merge_range(row, 4, row, 5, employee_detail.get('item', 0), center_align)
            sheet.merge_range(row, 6, row, 7, employee_detail.get('quantity', 0), center_align)
            sheet.merge_range(row, 8, row, 9, employee_detail.get('uom', 0), center_align)
            sheet.merge_range(row, 10, row, 11, employee_detail.get('price', 0), center_align)
            row += 1