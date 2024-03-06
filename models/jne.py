import requests
import logging
import json
import datetime

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

# list of endpoint that can be used in JNE https://apidash.jne.co.id/home
DESTINATION_URL = "%(protocol)s://apiv2.jne.co.id:%(port)s/insert/getdestination"
GET_ORIGIN_URL = "%(protocol)s://apiv2.jne.co.id:%(port)s/insert/getorigin"
TRACE_TRACKING_URL = "%(protocol)s://apiv2.jne.co.id:%(port)s/tracing/api/list/v1/cnote"
TARIFF_URL = "%(protocol)s://apiv2.jne.co.id:%(port)s/tracing/api/pricedev"
GENERATE_AWB_URL = "%(protocol)s://apiv2.jne.co.id:%(port)s/tracing/api/generatecnote"

class SSIJNE(models.Model):
    _name = "ssi.jne"
    _inherit = ['mail.thread']
    _description = "JNE Configuration"

    username = fields.Char(required=True)
    api_key = fields.Char(required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s (%s)" % (record.username, record.api_key)))
        
        return result

    def action_get_destination(self):
        """
        Do get destination
        """
        url = DESTINATION_URL

        response = self.do_request(url, "POST")
        return response
    
    def action_calculate_tarif_wizard(self):
        """
        open wizard calculate tarif JNE
        """
        return {
            "name": _("Check Tarif JNE"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "ssi.jne.tarif.wizard",
            "view_id": self.env.ref("ssi_jne.check_tarif_form_wizard").id,
            "target": "new",
            "context": {
                "default_jne_id": self.id,
            },
        }

    def action_calculation_tariff(self, params):
        """
        Do calcuclate tariff
        """
        url = TARIFF_URL

        # added params on body payload
        list_params = []
        for key, value in params.items():
            list_params.append("%s=%s" % (key, value))

        added_params = "&".join(list_params)
 
        response = self.do_request(url, "POST", added_params)
        return response

    def action_get_origin(self):

        """
        Do get origin
        """
        url = GET_ORIGIN_URL

        response = self.do_request(url, "POST")
        return response

    def _get_dummy_data_trace_tracking(self):
        return "5403212200022724"
    
    def action_trace_tracking_wizard(self):
        """
        Open pop up wizard for trace tracking data delivery
        """
        # use dummy data
        cnote = self._get_dummy_data_trace_tracking()
        
        return {
            "name": _("Trace Tracking Air Way Bill"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "ssi.jne.tracetracking.wizard",
            "view_id": self.env.ref("ssi_jne.trace_tracking_form_wizard").id,
            "target": "new",
            "context": {
                "default_jne_id": self.id,
                "default_cnote": cnote
            },
        }

    def action_trace_tracking(self, cnote):
        """
        Do trace tracking
        """
        url = TRACE_TRACKING_URL + "/%s" % (cnote)

        response = self.do_request(url, "POST")
        return response

    def _get_dummy_data_generate_awb(self, context):
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d%H%M%S")
        date_int = int(date_string)

        context["default_olshop_branch"] = "CGK000"
        context["default_olshop_cust"] = "TESTAKUN"
        context["default_olshop_orderid"] = "SSI%s" % (str(date_int))

        context["default_olshop_shipper_name"] = "ALI"
        context["default_olshop_shipper_addr1"] = "JAKARTA NO 44"
        context["default_olshop_shipper_addr2"] = "KALIBATA"
        context["default_olshop_shipper_addr3"] = "KALIBATA"
        context["default_olshop_shipper_city"] = "JAKARTA"
        context["default_olshop_shipper_region"] = "JAKARTA"
        context["default_olshop_shipper_zip"] = "12345"
        context["default_olshop_shipper_phone"] = "+6289876543212"

        context["default_olshop_receiver_name"] = "ANA"
        context["default_olshop_receiver_addr1"] = "BANDUNG NO 12"
        context["default_olshop_receiver_addr2"] = "CIBIRU"
        context["default_olshop_receiver_addr3"] = "BANDUNG"
        context["default_olshop_receiver_city"] = "BANDUNG"
        context["default_olshop_receiver_region"] = "JAWA BARAT"
        context["default_olshop_receiver_zip"] = "12365"
        context["default_olshop_receiver_phone"] = "+6285789065432"

        context["default_olshop_qty"] = "1"
        context["default_olshop_weight"] = "1" 
        context["default_olshop_goods_desc"] = "TEST" 
        context["default_olshop_goods_value"] = "1000"
        context["default_olshop_goods_type"] = "1"
        context["default_olshop_inst"] = "TEST"
        context["default_olshop_ins_flag"] = "N"
        context["default_olshop_orig"] = "CGK10000"
        context["default_olshop_dest"] = "BDO10000"
        context["default_olshop_service"] = "REG"
        context["default_olshop_cod_flag"] = "N"
        context["default_olshop_cod_amount"] = "0"

        return context

    def action_generate_awb_wizard(self):
        """
        open wizard calculate tarif JNE
        """
        context = {
            "default_jne_id": self.id,
        }

        # get dummy datas
        context = self._get_dummy_data_generate_awb(context)
        

        return {
            "name": _("Generate Air Way Bill"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "ssi.jne.awb.wizard",
            "view_id": self.env.ref("ssi_jne.generate_awb_form_wizard").id,
            "target": "new",
            "context": context,
        }

    def action_generate_awb(self, params):
        """
        Do generate air way bill
        """
        url = GENERATE_AWB_URL

        # added params on body payload
        list_params = []
        for key, value in params.items():
            list_params.append("%s=%s" % (key, value))

        added_params = "&".join(list_params)

        response = self.do_request(url, "POST", added_params)
        return response

    def _get_request_parameter(self, url):
        """
        preparing parameter to do http request
        """
        system_param = self.env["ir.config_parameter"].sudo()

        # required system parameters / ir.config_parameter
        protocol_url = system_param.get_param("ssi.jne_protocol_url")
        port_url = system_param.get_param("ssi.jne_port_url")

        if not protocol_url or not port_url:
            raise ValidationError(_("You need to set configuration in system parameter for ssi.jne_protocol_url (%s) and ssi.jne_port_url (%s)" % (
                protocol_url or "-",
                port_url or "-"
            )))
        
        # set protocol (https or http) and port on url, source: https://apidash.jne.co.id/see_docs/11
        # - sandbox/test server = protocol => http & port => 10102
        # - live server = protocol => https & port => 10205

        api_url = url % {
            "protocol": protocol_url,
            "port": port_url,
        }
        
        payload = "username=%s&api_key=%s" % (
            self.username,
            self.api_key
        ) 

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        result = {
            "url": api_url,
            "payload": payload,
            "headers": headers,
        }

        return result
        
    def do_request(self, url, method, added_params=None):
        """
        Main function to do http request to public API JNE
        """
        get_param = self._get_request_parameter(url)

        payload = get_param["payload"]
        if added_params:
            payload = "%s&%s" % (get_param["payload"], added_params)

        try:
            # do request
            response = requests.request(method, get_param["url"], headers=get_param["headers"], data=payload)
            response.raise_for_status()

            # Get the response
            result = json.loads(response.content)
            if result.get("error"):
                raise ValidationError(_("%s" % (result.get("error"))))
            
            return result
        except Exception as e:
            raise ValidationError(_("failed when do http request to url %s, method: %s, error: %s" % (
                get_param["url"], 
                method, 
                str(e)
            )))
        