# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Custom Model",
    "version": "16.0.0.0",
    "depends": ['base','contacts'],
    "author": "Ahmad Shahin",
    "summary": "Hide pager counter in contact",
    "description": """Hide pager counter in contact""",
    'category': 'Extra Rights',
    'price': 0,
    'currency': "EUR",
    "website": "https://www.youtube.com/@ahmad-odoo-apps",
    "data": [
        'security/security.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_model/static/src/js/hide_pager_counter.js'
        ],
    },
    "auto_install": False,
    "installable": True,
    "application": False,
    'live_test_url': 'https://www.youtube.com/@ahmad-odoo-apps',
    "images": ['static/description/icon2.png'],
    "license": 'OPL-1',
}