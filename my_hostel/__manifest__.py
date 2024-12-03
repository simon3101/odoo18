{
    'name': "Hostel Management",
    'summary': 'Manage Hostel easily',
    'description': "Efficiently manage the entire residential facility in the school.",
    'author': "SoftHard",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0',
    'depends': ['base'],
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/res_partner.xml",
        "views/hostel_view.xml",
        "views/room_view.xml",
        "views/student_view.xml",
        "views/amenitie.xml",
        "views/categoy_view.xml",
        "views/room_copy.xml",
        "views/actions.xml",
        "views/menus.xml"
	],
    'assets': {
        #'web.assets_backend': ['web/static/src/xml/**/*',],
    },
    #'demo': ['demo.xml'],
}
