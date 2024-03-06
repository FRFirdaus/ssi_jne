from odoo import api, models, fields

class SSIJNEDestination(models.Model):
    _name = "ssi.jne.destination"
    _description = "JNE Destination"

    name = fields.Char(required=True, string="Tariff Code")
    country = fields.Char()
    province = fields.Char()
    city = fields.Char()
    district = fields.Char()
    sub_district = fields.Char()
    zip = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s | (%s) %s / %s / %s / %s (ZIP: %s)" % (
                record.name,
                record.country,
                record.province,
                record.city or "-",
                record.district or "-",
                record.sub_district or "-",
                record.zip or "-"
            )))
        
        return result