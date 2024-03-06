from odoo import api, models, fields

class SSIJNEOrigin(models.Model):
    _name = "ssi.jne.origin"
    _description = "JNE Origin"

    name = fields.Char(required=True)
    code = fields.Char(required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "[%s] %s" % (
                record.code,
                record.name
            )))
        
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search([('code', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(SSIJNEOrigin, self).name_search(name=name, args=args,
                                                    operator=operator,
                                                    limit=limit)
        return recs.name_get()