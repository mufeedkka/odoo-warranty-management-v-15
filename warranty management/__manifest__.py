{
    'name': 'Warranty',
    'description': 'warranty',
    'version': '15.0.1.0.0',
    'installable': True,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/warranty_security.xml',
        'data/location_creation.xml',
        'views/warranty.xml',
        'views/stock_move.xml',
        'views/project_inherit.xml',
        'wizard/settings_wizard.xml',
        'reports/report.xml',
        'reports/product_warranty.xml',


    ],
    'assets': {
        'web.assets_backend': [
            'warranty/static/src/js/action_manager.js',
        ],
    },
    'depends': [
        'stock',
        'account',
        'sale',
        'base',
        'mail',
    ]
}
