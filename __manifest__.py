# -*- coding: utf-8 -*-
{
    'name': "WFZ Academy",

    'summary': """
        Learning Odoo development with Kevin,
        Enjoy the fun with Odoo""",

    'description': """
        This module covers nearly all sides of a module, from class to reports,
        it is a good way for you to learn.
    """,

    'author': "Kevin Li",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'education',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','board'],

    # always loaded
    'date': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        # 'views/session_workflow.xml',
        'views/session_board.xml',
        'reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}