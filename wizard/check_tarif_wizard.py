from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class JNETarifWizard(models.TransientModel):
    _name = "ssi.jne.tarif.wizard"
    _description = "Check Tarif JNE Wizard"

    jne_id = fields.Many2one("ssi.jne")
    origin_id = fields.Many2one("ssi.jne.origin")
    destination_id = fields.Many2one("ssi.jne.destination")
    weight = fields.Float()

    line_ids = fields.One2many("ssi.jne.tarif.line.wizard", "tarif_wiz_id")

    @api.onchange("jne_id", "origin_id", "destination_id", "weight")
    def _onchange_check_tarif(self):
        # clean tarif line
        self.line_ids = [(5, 0, 0)]

        # check if all fields has value
        if self.jne_id and self.origin_id and self.destination_id and self.weight:
            payload = {
                "from": self.origin_id.code,
                "thru": self.destination_id.name,
                "weight": self.weight,
            }

            # do http request to get tarif datas
            response = self.jne_id.action_calculation_tariff(payload)

            # if there are no field price on response raise error
            prices = response.get("price")
            if not prices:
                raise ValidationError(_("There are no service from %s to %s" % (payload["source"], payload["destination"])))


            # added list of tarif on tarif checking line
            price_datas = [(0, 0, {
                "tarif_wiz_id": self.id,
                "origin": price["origin_name"],
                "destination": price["destination_name"],
                "service": price["service_display"],
                "service_code": price["service_code"],
                "goods_type": price["goods_type"],
                "currency": price["currency"],
                "price": price["price"],
                "etd_from": price["etd_from"],
                "etd_thru": price["etd_thru"],
                "times": price["times"],
            }) for price in prices]

            self.line_ids = price_datas

    def check_tarif(self):
        context = self._context
        payload = {
            "from": self.origin_id.code,
            "thru": self.destination_id.name,
            "weight": self.weight,
        }

        # do http request to get tarif datas
        response = self.jne_id.action_calculation_tariff(payload)

        # if there are no field price on response raise error
        prices = response.get("price")
        if not prices:
            raise ValidationError(_("There are no service from %s to %s" % (payload["source"], payload["destination"])))

        # posted on active model and data like sale order, purchase order, delivery order, etc
        if context.get("active_model") and context.get("active_id"):
            try:
                # preparing list of tarif data to be posted in message log
                list_of_price = ["<p>\u2022 <b>Origin:</b> %s, <b>Destination:</b> %s, <b>Service:</b> %s [Code: %s], <b>Goods Type:</b> %s, <b>Currency:</b> %s, <b>Price:</b> %s, <b>ETD From:</b> %s, <b>ETD Thru:</b> %s, <b>Times:</b> %s</p>" % (
                    price["origin_name"],
                    price["destination_name"],
                    price["service_display"],
                    price["service_code"],
                    price["goods_type"],
                    price["currency"],
                    price["price"],
                    price["etd_from"],
                    price["etd_thru"],
                    price["times"]
                ) for price in prices]
                
                body_message = "<h3>LIST TARIF JNE<br/><br/>From: %s<br/><br/> To: %s<br/><br/>Weight: %s Kg</h3><br/>%s" % (
                    self.origin_id.display_name,
                    self.destination_id.display_name,
                    payload["weight"],
                    "<br/>".join(list_of_price)
                )

                model_data_id = self.env[context.get("active_model")].browse(int(context.get("active_id")))
                model_data_id.message_post(body=body_message)
            except Exception as e:
                pass

class JNETarifLineWizard(models.TransientModel):
    _name = "ssi.jne.tarif.line.wizard"
    _description = "Check Tarif JNE Line Wizard"

    tarif_wiz_id = fields.Many2one("ssi.jne.tarif.wizard")
    origin = fields.Char(string="Origin/Source")
    destination = fields.Char()
    service = fields.Char()
    service_code = fields.Char()
    goods_type = fields.Char()
    currency = fields.Char()
    price = fields.Char()
    etd_from = fields.Char()
    etd_thru = fields.Char()
    times = fields.Char()


