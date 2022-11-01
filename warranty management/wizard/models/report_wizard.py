from odoo import models, fields
from  odoo.tools import date_utils
import  json
import io
import  xlsxwriter
class warranty_report(models.TransientModel):
    _name = 'warranty.report'
    _description = 'warranty report'

    product_ids = fields.Many2many('product.product',domain="[('warranty_enable', '=', 'True')]")
    customer_id = fields.Many2one('res.partner')
    start_date = fields.Date()
    end_date = fields.Date()


    def print_report(self):
        # a = self.read()
        # print(a)
        length = len(self.product_ids)
        print(length)
        if self.customer_id and length>1:
            print("if 1")

            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id in %s and warranty.customer_name_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids.ids),
                self.customer_id.id,
                self.start_date,
                self.end_date))


            result = self.env.cr.dictfetchall()
            print(result)

            data = {
                'result': result,
            }
            return self.env.ref(
                'warranty.warranty_report_print').report_action(None,data=data)

        elif self.customer_id and length<=1:
            print("if 2")

            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id = %s and warranty.customer_name_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                self.product_ids.id,
                self.customer_id.id,
                self.start_date,
                self.end_date))


            result = self.env.cr.dictfetchall()
            print(result)

            data = {
                'result': result,
            }
            return self.env.ref(
                'warranty.warranty_report_print').report_action(None,data=data)

        elif not self.customer_id and length<=1:
            print("if 3")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                self.product_ids.id,
                self.start_date,
                self.end_date))


            result = self.env.cr.dictfetchall()
            print(result)

            data = {
                'result': result,
            }
            return self.env.ref(
                'warranty.warranty_report_print').report_action(None,data=data)
        elif self.customer_id == False and length>1:
            print("if 4")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id in %s
            and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids),
                self.start_date,
                self.end_date))


            result = self.env.cr.dictfetchall()
            print(result)

            data = {
                'result': result,
            }
            return self.env.ref(
                'warranty.warranty_report_print').report_action(None,data=data)

        else:
            print("else")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
                        product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
                        on warranty.customer_name_id=res_partner.id join product_product on 
                        warranty.product_id=product_product.id join account_move on 
                        warranty.invoice_id = account_move.id join stock_production_lot on 
                        warranty.lot_serial_number_id = stock_production_lot.id join 
                        product_template on product_product.product_tmpl_id = product_template.id where 
                        warranty.product_id in %s
                        and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids.ids),
                self.start_date,
                self.end_date))

            result = self.env.cr.dictfetchall()
            print(result)

            data = {
                'result': result,
            }
            return self.env.ref(
                'warranty.warranty_report_print').report_action(None,
                                                                data=data)
    def print_xls(self):
        length = len(self.product_ids)
        print(length)
        if self.customer_id and length > 1:
            print("if 1")

            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id in %s and warranty.customer_name_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids.ids),
                self.customer_id.id,
                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        elif self.customer_id and length == 1 :
            print("if 2")

            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id = %s and warranty.customer_name_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                self.product_ids.id,
                self.customer_id.id,
                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        elif not self.customer_id and length==1:
            print("if 3")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id = %s 
            and request_date > '%s' and request_date < '%s' """ % (
                self.product_ids.id,
                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        elif self.customer_id == False and length>1:
            print("if 4")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            warranty.product_id in %s
            and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids),
                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        elif not self.product_ids:
            print("if 5")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            request_date > '%s' and request_date < '%s' """ % (

                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        elif self.customer_id == False:
            print("if 5")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
            product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
            on warranty.customer_name_id=res_partner.id join product_product on 
            warranty.product_id=product_product.id join account_move on 
            warranty.invoice_id = account_move.id join stock_production_lot on 
            warranty.lot_serial_number_id = stock_production_lot.id join 
            product_template on product_product.product_tmpl_id = product_template.id where 
            request_date > '%s' and request_date < '%s' """ % (

                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)
        else:
            print("else")
            self.env.cr.execute(""" SELECT warranty.name as name,res_partner.name as custname,
                        product_template.name as productname,account_move.name as invoicename,stock_production_lot.name as lotname,warranty.state FROM warranty join res_partner 
                        on warranty.customer_name_id=res_partner.id join product_product on 
                        warranty.product_id=product_product.id join account_move on 
                        warranty.invoice_id = account_move.id join stock_production_lot on 
                        warranty.lot_serial_number_id = stock_production_lot.id join 
                        product_template on product_product.product_tmpl_id = product_template.id where 
                        warranty.product_id in %s
                        and request_date > '%s' and request_date < '%s' """ % (
                tuple(self.product_ids.ids),
                self.start_date,
                self.end_date))
            result = self.env.cr.dictfetchall()
            print(result)




        # data = {
        #     'result': result,
        # }
        data = {
            'result': result,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        print("print xls")
        return {'type': 'ir.actions.report',
                'data': {
                        'model': 'warranty.report',
                        'options': json.dumps(data,
                                               default=date_utils.json_default),
                        'output_format': 'xlsx',
                        'report_name': 'Excel Report Name', },

                'report_type': 'xlsx'
                }

    def get_xlsx_report(self, data, response):
        result = data['result']
        print(result)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('G2:M3', 'PRODUCT WARRANTY REPORT', head)
        sheet.write('G6', 'From:', cell_format)
        sheet.merge_range('H6:I6', data['start_date'], txt)
        sheet.write('K6', 'To:', cell_format)
        sheet.merge_range('L6:M6', data['end_date'], txt)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 15)
        sheet.set_column('G:G', 10)
        row = 9
        col = 6
        sheet.write(row, col,'Name')
        sheet.write(row, col+1,'custname')
        sheet.write(row, col+2,'productname')
        sheet.write(row, col+3,'invoicename')
        sheet.write(row, col+4,'lotname')
        sheet.write(row, col+5,'state')

        for i in result:
            print(i)
            row = row+1
            sheet.write(row, col, i['name'])
            sheet.write(row, col + 1, i['custname'])
            sheet.write(row, col + 2, i['productname'])
            sheet.write(row, col + 3, i['invoicename'])
            sheet.write(row, col + 4, i['lotname'])
            sheet.write(row, col + 5, i['state'])
        # # new
        # sheet.write('B6', 'From:', cell_format)
        # sheet.merge_range('C6:D6', data['start_date'], txt)
        # sheet.write('F6', 'To:', cell_format)
        # sheet.merge_range('G6:H6', data   ['end_date'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()