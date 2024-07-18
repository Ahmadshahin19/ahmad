# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Apps One",
    "version": "17.0.0.0",
    "depends": ['base','sale'],
    "author": "Ahmad Shahin",
    "summary": "Test One Apps",
    "description": """ test 2""",
    'category': 'Accounting',
    'price': 5,
    'currency': "EUR",
    "website": "http://localhost:8070/web/database/selector",
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv', # هاذا الفيلد لازم يكون اسمه نفس اسم مديول الصلاحيات مهم جدا
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/property_history_view.xml',
        'reports/property_reports.xml',
        'wizard/change_state_wizard_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [

        ],
        'web.assets_backend': [
            'app_one/static/src/css/property.css'
        ],
        'web.report_assets_common': [
            'app_one/static/src/css/font.css'
        ],
    },
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
    'live_test_url': 'https://youtu.be/gOzKF-5IbCs?si=1Ebp702cLXx1b0vw',
    "images": ['static/description/icon2.png'],
    "license": 'OPL-1',
}
