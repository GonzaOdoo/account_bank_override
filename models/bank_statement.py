from odoo import models,api,fields
import logging

_logger = logging.getLogger(__name__)
class BankStatement(models.Model):
    _inherit = "account.bank.statement.line"

    fake_amount = fields.Monetary('Monto')
    is_negative = fields.Selection([('debit','Ingreso'),('credit','Egreso')],string='Tipo',default='credit',required=True)
    bank_tag_id = fields.Many2one(
        comodel_name='bank.statement.tags',
        string='Etiqueta',
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string="Impuestos",
        store=True, readonly=False,
        check_company=True,
    )
    
    @api.onchange('fake_amount', 'is_negative')
    def _on_change_amount(self):
        for record in self:
            sign = -1 if record.is_negative == 'credit' else 1
            record.amount = sign * record.fake_amount


    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        """ Prepare the dictionary to create the default account.move.lines for the current account.bank.statement.line
        record.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        """
        self.ensure_one()

        if not counterpart_account_id:
            counterpart_account_id = self.bank_tag_id.suspense_account_id.id

        if not counterpart_account_id:
            raise UserError(_(
                "You can't create a new statement line without a suspense account set on the %s journal.",
                self.bank_tag_id.name,
            ))

        company_currency = self.journal_id.company_id.sudo().currency_id
        journal_currency = self.journal_id.currency_id or company_currency
        foreign_currency = self.foreign_currency_id or journal_currency or company_currency

        # Calcular el monto con impuestos
        tax_results = self.tax_ids.compute_all(
            self.amount_currency if foreign_currency != journal_currency else self.amount,
            currency=foreign_currency,
            quantity=1.0,
            product=None,
            partner=self.partner_id
        )
        total_with_tax = tax_results['total_included']

        journal_amount = self.amount
        if foreign_currency == journal_currency:
            transaction_amount = journal_amount
            transaction_amount_with_tax = total_with_tax
        else:
            transaction_amount = self.amount_currency
            transaction_amount_with_tax = total_with_tax
    
        if journal_currency == company_currency:
            company_amount = journal_amount
            company_amount_with_tax = total_with_tax
        elif foreign_currency == company_currency:
            company_amount = transaction_amount
            company_amount_with_tax = transaction_amount_with_tax
        else:
            company_amount = journal_currency\
                ._convert(journal_amount, company_currency, self.journal_id.company_id, self.date)
            company_amount_with_tax = journal_currency\
                ._convert(total_with_tax, company_currency, self.journal_id.company_id, self.date)

        liquidity_line_vals = {
            'name': self.bank_tag_id.name,
            'move_id': self.move_id.id,
            'partner_id': self.partner_id.id,
            'account_id': self.journal_id.default_account_id.id,
            'currency_id': journal_currency.id,
            'amount_currency': total_with_tax if foreign_currency == journal_currency else journal_amount,
            'debit': company_amount_with_tax > 0 and company_amount_with_tax or 0.0,
            'credit': company_amount_with_tax < 0 and -company_amount_with_tax or 0.0,
        }

        # Create the counterpart line values.
        counterpart_line_vals = {
            'name': self.bank_tag_id.name,
            'account_id': counterpart_account_id,
            'move_id': self.move_id.id,
            'partner_id': self.partner_id.id,
            'currency_id': foreign_currency.id,
            'tax_ids': [(6, 0, self.tax_ids.ids)],
            'amount_currency': -transaction_amount,
            'debit': -company_amount if company_amount < 0.0 else 0.0,
            'credit': company_amount if company_amount > 0.0 else 0.0,
        }
        return [liquidity_line_vals, counterpart_line_vals]
