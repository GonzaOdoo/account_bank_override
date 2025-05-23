# -*- coding: utf-8 -*-
{
    'name': "Modificacion de pantalla de transaccion bancaria",

    'summary': """
        Este modulo modifica la pantalla de nueva transaccion bancaria, añadiendo nuevos campos y funcionalidades""",

    'description': """
        Este modulo modifica la pantalla de nueva transaccion bancaria, añadiendo nuevos campos y funcionalidades
    """,

    'author': "GonzaOdoo",
    'website': "https://github.com/GonzaOdoo",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant','account'],

    'data':[
        'security/ir.model.access.csv',
        'views/bank_rec_widget_views.xml',
        'views/bank_tags.xml',
        'views/account_journal_views.xml',
    ]

}