{
    'name': 'Account move',
    'version': '18.0',
    'summary': 'inherit account.move',
    'description': 'this module is to inherit account.move',
    'author': 'simon',
    'depends': ['account'],  # Depende del módulo account
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'account_move/static/src/components/tax_totals/tax_totals.xml',
        ],
    },
}