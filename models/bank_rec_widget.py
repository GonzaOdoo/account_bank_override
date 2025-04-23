from odoo import models,fields,api
import json

class BankRecWidget(models.Model):
    _inherit='bank.rec.widget'

    @api.model
    def collect_global_info_data(self, journal_id):
        journal = self.env['account.journal'].browse(journal_id)
        balance = ''
        if journal.exists() and any(company in journal.company_id._accessible_branches() for company in self.env.companies):
            # Parsear el kanban_dashboard para obtener account_balance
            try:
                dashboard_data = json.loads(journal.kanban_dashboard)
                balance = dashboard_data.get('account_balance', '')
            except (json.JSONDecodeError, AttributeError):
                # Si hay error al parsear o no existe el campo, usar el valor original
                balance = formatLang(self.env,
                                    journal.current_statement_balance,
                                    currency_obj=journal.currency_id or journal.company_id.sudo().currency_id)
        return {'balance_amount': balance}