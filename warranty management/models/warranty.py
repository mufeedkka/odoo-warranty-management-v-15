from odoo import models, fields, api, _
from odoo.exceptions import UserError

# class StockFunction(models.Model):
#     _inherit = 'stock.picking'
#
#     def action_confirm(self):
#         request = self.env['stock.picking'].search([('origin', '=', self.origin)])
#         print(self.origin)
#         request.state = 'assigned'
#         res = super(StockFunction, self).action_confirm()
#         print("action done")
#         return res


class Warranty(models.Model):
    _name = "warranty"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Warranty"

    name = fields.Char(required=True, copy=False, readonly=True,
                       default=_('New'))
    customer_name_id = fields.Many2one("res.partner")
    # street = fields.Char(related='customer_name.street')
    invoice_id = fields.Many2one('account.move',
                                 domain="[('state', '=', 'posted')]")
    product_id = fields.Many2one('product.product')

    @api.onchange("invoice_id")
    def _onchange_invoice_id(self):
        print("working inv")
        list = []
        for i in self.invoice_id.invoice_line_ids.product_id:
            invoice_product_id = int(i)
            print(type(invoice_product_id))
            print(invoice_product_id)
            list.append(invoice_product_id)
            print(list)
        return {'domain': {'product_id': [('id', '=', list)]}}

    @api.onchange('customer_name_id')
    def _onchange_customer_name_id(self):
        print("invoice fetch working")
        partner_id = int(self.customer_name_id)
        return {'domain': {'invoice_id': [('state', '=', 'posted'),
                                          ('partner_id', '=', partner_id)]}}


    @api.onchange('product_id')
    def _onchange_product_id(self):
        print("lot and serial working")
        print(self.product_id.id)
        # product_test = self.env['stock.picking']
        product_id_invoice = int(self.product_id.id)

        print("warranty is working")
        print(self.product_id.warranty_period_id)
        period = int(self.product_id.warranty_period_id)
        print("invoice date", self.invoice_id.invoice_date)
        invoice_date = self.invoice_id.invoice_date
        if invoice_date:
            exp_date = fields.Date.add(
                invoice_date, days=period
            )

            print(exp_date)
            self.warranty_exp = exp_date
        return {'domain': {'lot_serial_number_id':
                               [('product_id', '=', product_id_invoice)]}}

    lot_serial_number_id = fields.Many2one('stock.production.lot',
                                           string="lot & serial number")
    request_date = fields.Date(default=fields.Date.today())
    purchase_date = fields.Date(string='Purchase Date',
                                related='invoice_id.date')
    warranty_exp = fields.Date()
    invoice_inverse_ids = fields.One2many('account.move', 'war_info_id')
    warranty_period_id = fields.Many2one('product.template')

    state = fields.Selection(
        [('draft', 'Draft'), ('to approve', 'To approve'),
         ('approved', 'Approved'),
         ('product received', 'Product received'),
         ('done', 'Done'),
         ('cancel', 'Cancel')], default='draft')

    # @api.onchange("product_id")
    # def war(self):
    #     print("warranty is working")
    #     print(self.product_id.warranty_period_id)
    #     period = int(self.product_id.warranty_period_id)
    #     print("invoice date", self.invoice_id.invoice_date)
    #     invoice_date = self.invoice_id.invoice_date
    #     if invoice_date:
    #         exp_date = fields.Date.add(
    #             invoice_date, days=period
    #         )
    #
    #         print(exp_date)
    #         self.warranty_exp = exp_date

    def warranty_stock_move(self):
        print("smart button function working name is stock_move")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warranty stock move',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)],
            'view_mode': 'tree,form',

        }



    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'Warranty.seq') or 'New'
        res = super(Warranty, self).create(vals)
        return res

    def change_state_approved(self):
        print("approved working")
        self.state = 'approved'
        warranty_id = int(self.env['stock.location'].search([
            ('complete_name', '=', 'warranty')
        ]))
        customer_loc_id = int(self.env['stock.location'].search([
            ('complete_name', '=', 'Partner Locations/Customers')
        ]))
        vals = []
        print("lot",self.lot_serial_number_id.id)
        vals.append((0, 0,
                     {'product_id': self.product_id.id,
                      'name': self.product_id.name,
                      'product_uom': 1,
                          # 'product_uom_qty': 1,
                      # 'quantity_done': 0,
                      'location_id': customer_loc_id,
                      'location_dest_id': warranty_id,
                      'lot_ids': [(6, 0, [self.lot_serial_number_id.id])],
                      }))
        # [(6, 0, [self.lot_serial_number_id.name])]
        print(warranty_id, "it is warranty location")
        print(customer_loc_id, "it is customer location")
        print(self.lot_serial_number_id.name)
        self.env['stock.picking'].create({
            'product_id': self.product_id.id,
            'partner_id': self.customer_name_id.id,
            'origin': self.name,
            # 'lot_id': lot_or_serial,
            'location_id': customer_loc_id,
            'location_dest_id': warranty_id,
            # 'company_id': 1,
            'picking_type_id': 7,
            'move_ids_without_package': vals,

        })

    def change_state_toapprove(self):
        self.state = 'to approve'
        print(self.product_id.warranty_enable)
        if self.product_id.warranty_enable == False:
            print("it is not warranty product")
            raise UserError("Its is not warranty product")
        else:
            print("it is warranty product")
            if self.warranty_exp <= fields.Date.today():
                raise UserError("Warranty Expired")

    def change_state_cancel(self):
        self.state = 'cancel'

    def change_state_product_recived(self):
        self.state = 'product received'
        stockpick = self.env['stock.picking'].search([('origin', '=', self.name)])
        stockpick.state = 'assigned'
        stockpick.action_confirm()
        print("action confirm")
        stockpick.button_validate()
        st = self.env['stock.picking'].browse(
            [self._context.get('active_id')])
        print(st, "active_id")

    def change_state_done(self):
        self.state = 'done'


        lot_or_serial = int(self.lot_serial_number_id)
        print(self.product_id.warranty_type)
        warranty_id = int(self.env['stock.location'].search([
            ('complete_name', '=', 'warranty')
        ]))
        customer_loc_id = int(self.env['stock.location'].search([
            ('complete_name', '=', 'Partner Locations/Customers')
        ]))
        stock_loc_id = int(self.env['stock.location'].search([
            ('complete_name', '=', 'WH/Stock')
        ]))
        print(warranty_id, "it is warranty location")
        print(customer_loc_id, "it is customer location")
        print(stock_loc_id, "it is stock location")
        product_warranty_type = self.product_id.warranty_type
        vals = []
        vals.append((0, 0,
                     {'product_id': self.product_id.id,
                      'name': self.product_id.name,
                      'product_uom': 1 ,
                      'location_id': stock_loc_id,
                      'location_dest_id': customer_loc_id,
                      'lot_ids': [(6, 0, [self.lot_serial_number_id.id])],
                      }))
        if product_warranty_type == "Replacement warranty":
            print("replacement product")

            self.env['stock.picking'].create({
                'product_id': self.product_id.id,
                'partner_id': self.customer_name_id.id,
                'origin': self.name,
                # 'lot_id': lot_or_serial,
                'location_id': stock_loc_id,
                'location_dest_id': customer_loc_id,
                # 'company_id': 1,
                'picking_type_id': 8,
                'move_ids_without_package': vals,
            })
            stockpick = self.env['stock.picking'].search(
                [('origin', '=', self.name)])
            # stockpick.state = 'assigned'
            stockpick.action_confirm()
            print("assigned")
            # stockpick.button_validate()
        else:
            print("service type product")
            vals_in_service_product = []
            vals_in_service_product.append((0, 0,
                                            {'product_id': self.product_id.id,
                                             'name': self.product_id.name,
                                             'product_uom': 1,
                                             # 'product_uom_qty': 1,
                                             # 'quantity_done': 1,
                                             'location_id': warranty_id,
                                             'location_dest_id': customer_loc_id,
                                             'lot_ids': [(6, 0, [self.lot_serial_number_id.id])],
                                             }))
            print(vals_in_service_product)
            self.env['stock.picking'].create({
                'product_id': self.product_id.id,
                'partner_id': self.customer_name_id.id,
                'origin': self.name,
                # 'lot_id': lot_or_serial,
                'location_id': warranty_id,
                'location_dest_id': customer_loc_id,
                # 'company_id': 1,
                'picking_type_id': 8,
                'move_ids_without_package': vals_in_service_product,
            })


            stockpick = self.env['stock.picking'].search(
                [('origin', '=', self.name)])
            # stockpick.state = 'assigned'
            stockpick.action_confirm()
            print("assigned")
            # stockpick.button_validate()





class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty_period_id = fields.Integer()
    warranty_type = fields.Selection([('Service Warranty', 'Service Warranty'),
                                      ('Replacement warranty',
                                       'Replacement warranty')])
    warranty_enable = fields.Boolean()


class WarrantyInfo(models.Model):
    _inherit = 'account.move'

    war_info_id = fields.One2many('warranty', 'invoice_id')





