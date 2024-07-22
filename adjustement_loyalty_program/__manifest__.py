# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Alpha Report',
    'version': '1.1.0',
    'summary': 'Coupons',
    'sequence': 10,
    'description': """
    Rapport génerale
    """,
    'category': 'sale',
    'depends': ['base', 'sale'],
    'data': [
        'views/all_view_partner.xml',
      ],
    'installable': True,
}
