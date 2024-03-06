# -*- coding: utf-8 -*-
{
    'name': 'SSI JNE',
    'summary': 'JNE master module.',

    'author': 'Fahmi Roihanul Firdaus',
    'website': 'https://www.linkedin.com/in/fahmi-roihanul-firdaus-05749416b/',
    'description': '''Features:

* JNE connection settings
* JNE master data settings''',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'base'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/jne_views.xml',
        'views/jne_dest_views.xml',
        'views/jne_branch_views.xml',
        'views/jne_origin_views.xml',
        'views/menu_views.xml',
        'wizard/check_tarif_views.xml',
        'wizard/generate_air_way_bill_views.xml',
        'wizard/trace_tracking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],

    # license and application info
    'license': 'LGPL-3',
}
