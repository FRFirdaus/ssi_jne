from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class GenerateAWBWizard(models.TransientModel):
    _name = "ssi.jne.awb.wizard"
    _description = "Generate AWB (Air Way Bill) Wizard"

    jne_id = fields.Many2one("ssi.jne")
    origin_id = fields.Many2one("ssi.jne.origin")
    destination_id = fields.Many2one("ssi.jne.destination")
    branch_id = fields.Many2one("ssi.jne.branch")

    olshop_branch = fields.Char()
    olshop_cust = fields.Char()
    olshop_orderid = fields.Char()
    
    olshop_shipper_name = fields.Char()
    olshop_shipper_addr1 = fields.Char()
    olshop_shipper_addr2 = fields.Char()
    olshop_shipper_addr3 = fields.Char()
    olshop_shipper_city = fields.Char()
    olshop_shipper_region = fields.Char()
    olshop_shipper_zip = fields.Char()
    olshop_shipper_phone = fields.Char()
    
    olshop_receiver_name = fields.Char()
    olshop_receiver_addr1 = fields.Char()
    olshop_receiver_addr2 = fields.Char()
    olshop_receiver_addr3 = fields.Char()
    olshop_receiver_city = fields.Char()
    olshop_receiver_region = fields.Char()
    olshop_receiver_zip = fields.Char()
    olshop_receiver_phone = fields.Char()
    
    olshop_qty = fields.Float()
    olshop_weight = fields.Float()
    
    olshop_goods_desc = fields.Text()
    olshop_goods_value = fields.Char()
    olshop_goods_type = fields.Char()

    olshop_inst = fields.Text()
    olshop_ins_flag = fields.Char()
    olshop_orig = fields.Char()
    olshop_dest = fields.Char()
    
    olshop_service = fields.Char()
    olshop_cod_flag = fields.Char()
    olshop_cod_amount = fields.Char()

    @api.onchange("jne_id", "branch_id")
    def _onchange_set_branch_code(self):
        if self.jne_id and self.branch_id:
            self.olshop_branch = self.branch_id.code

    @api.onchange("jne_id", "origin_id")
    def _onchange_set_origin_code(self):
        if self.jne_id and self.origin_id:
            self.olshop_orig = self.origin_id.code
        
    @api.onchange("jne_id", "destination_id")
    def _onchange_set_destination_code(self):
        if self.jne_id and self.destination_id:
            self.olshop_dest = self.destination_id.name

    def Generate_awb(self):
        """
        Generate AWB to get cnote
        """
        context = self._context

        # prepare initial payload
        payload = {
            "OLSHOP_BRANCH": self.olshop_branch,
            "OLSHOP_CUST": self.olshop_cust,
            "OLSHOP_ORDERID": self.olshop_orderid,
            "OLSHOP_SHIPPER_NAME": self.olshop_shipper_name,
            "OLSHOP_SHIPPER_ADDR1": self.olshop_shipper_addr1,
            "OLSHOP_SHIPPER_ADDR2": self.olshop_shipper_addr2,
            "OLSHOP_SHIPPER_ADDR3": self.olshop_shipper_addr3,
            "OLSHOP_SHIPPER_CITY": self.olshop_shipper_city,
            "OLSHOP_SHIPPER_REGION": self.olshop_shipper_region,
            "OLSHOP_SHIPPER_ZIP": self.olshop_shipper_zip,
            "OLSHOP_SHIPPER_PHONE": self.olshop_shipper_phone,
            "OLSHOP_RECEIVER_NAME": self.olshop_receiver_name,
            "OLSHOP_RECEIVER_ADDR1": self.olshop_receiver_addr1,
            "OLSHOP_RECEIVER_ADDR2": self.olshop_receiver_addr2,
            "OLSHOP_RECEIVER_ADDR3": self.olshop_receiver_addr3,
            "OLSHOP_RECEIVER_CITY": self.olshop_receiver_city,
            "OLSHOP_RECEIVER_REGION": self.olshop_receiver_region,
            "OLSHOP_RECEIVER_ZIP": self.olshop_receiver_zip,
            "OLSHOP_RECEIVER_PHONE": self.olshop_receiver_phone,
            "OLSHOP_QTY": self.olshop_qty,
            "OLSHOP_WEIGHT": self.olshop_weight,
            "OLSHOP_GOODSDESC": self.olshop_goods_desc,
            "OLSHOP_GOODSVALUE": self.olshop_goods_value,
            "OLSHOP_GOODSTYPE": self.olshop_goods_type,
            "OLSHOP_INST": self.olshop_inst,
            "OLSHOP_INS_FLAG": self.olshop_ins_flag,
            "OLSHOP_ORIG": self.olshop_orig,
            "OLSHOP_DEST": self.olshop_dest,
            "OLSHOP_SERVICE": self.olshop_service,
            "OLSHOP_COD_FLAG": self.olshop_cod_flag,
            "OLSHOP_COD_AMOUNT": self.olshop_cod_amount,
        }

        # do http request to generate awb data
        response = self.jne_id.action_generate_awb(payload)

        # post data response on message log
        if context.get("active_model") and context.get("active_id"):
            try:
                body_message = "Generate Air Way Bill: %s" % (response)
                model_data_id = self.env[context.get("active_model")].browse(int(context.get("active_id")))
                model_data_id.message_post(body=body_message)
            except Exception as e:
                pass

