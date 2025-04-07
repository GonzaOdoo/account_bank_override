from odoo import models,api,fields

class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    special_transaction = fields.Boolean(
        string="Transacción Bancaria Avanzada",
        help="Esta opcion habilita las transacciones bancarias modificadas.",
    )

