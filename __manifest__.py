# -*- coding: utf-8 -*-
{
    'name': "Modificacion de pantalla de transaccion",

    'summary': """
        Este modulo modifica la pantalla de nueva transaccion bancaria, añadiendo nuevos campos y funcionalidades""",

    'description': """
        Este modulo modifica la pantalla de nueva transaccion bancaria, añadiendo nuevos campos y funcionalidades
    """,

    'author': "GonzaOdoo",
    'website': "https://github.com/GonzaOdoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    'data':[
        'security/ir.model.access.csv',
        'views/bank_rec_widget_views.xml',
        'views/bank_tags.xml',
    ]

}