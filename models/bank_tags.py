from odoo import models,fields,api
import logging

_logger = logging.getLogger(__name__)
class BankStatementTags(models.Model):
    _name = 'bank.statement.tags'

    company_id = fields.Many2one('res.company',string="Empresa", required=True, default=lambda self: self.env.company)
    name = fields.Char('Nombre')

    suspense_account_id = fields.Many2one(
        comodel_name='account.account', check_company=True, 
        ondelete='restrict', 
        readonly=False, 
        store=True,
        string = 'Cuenta transitoria',
        domain = "[('deprecated', '=', False)]",
    )
    