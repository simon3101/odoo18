{
    'name': "Views Odoo",
    'summary': "views in odoo",
    'description': "Knowing all diffent views in odoo",  # Supports reStructuredText(RST) format (description is Deprecated)
    'author': "Simon",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'data': [
        'security/views_security.xml',
        'security/ir.model.access.csv',
        'views/view_model.xml',
    ],
    'assets': {
    },
}