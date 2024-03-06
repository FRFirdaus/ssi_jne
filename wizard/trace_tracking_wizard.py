from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class TraceTrackingWizard(models.TransientModel):
    _name = "ssi.jne.tracetracking.wizard"
    _description = "Trace Tracking Wizard"

    jne_id = fields.Many2one("ssi.jne")
    cnote = fields.Char(string="CNOTE")

    def do_trace_tracking(self):
        """
        Trace Tracking by cnote
        """
        context = self._context
        cnote = self.cnote
        # do http request to trace tracking datas
        response = self.jne_id.action_trace_tracking(cnote)

        body_message = "Trace Tracking: %s" % (response)
        if context.get("active_model") and context.get("active_id"):
            model_data_id = self.env[context.get("active_model")].browse(int(context.get("active_id")))
            model_data_id.message_post(body=body_message)
