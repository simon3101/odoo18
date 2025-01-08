{
    'name': "Hostel Management",
    'summary': 'Manage Hostel easily',
    'description': "Efficiently manage the entire residential facility in the school.",
    'author': "SoftHard",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '18.0.1.2',
    'depends': ['base','web_cohort','web_gantt','mail','web_map'],
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/category_data.xml",
        "views/actions.xml",
        "views/res_partner.xml",
        "views/hostel_view.xml",  
        "views/student_view.xml",
        "views/amenitie.xml",
        "views/room_copy.xml",
        "views/categoy_view.xml",
        "views/room_view.xml",
        "views/hostel_room_availability.xml",
        "views/config_view.xml",
        "views/menus.xml",
        "wizards/assign_room_student_wizard_view.xml",
	],
    'assets':{
        #'web.assets_backend': ['web/static/src/xml/**/*',],
    },
    'demo': [
        'data/demo.xml',
    ],
    'pre_init_hook': 'pre_init_hook_hostel',
    'post_init_hook': 'add_room_hook',
    'uninstall_hook': 'uninstall_hook_user',
    'license': 'LGPL-3'
}

