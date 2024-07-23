# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class LoyaltyProgram(models.Model):
    """To set the point rate when change is converted to loyalty points"""
    _inherit = 'loyalty.program'

    nbr_coupon_util = fields.Integer(string='Nombre de coupons utilisés', compute="_calcule_nbr_coupon_util",
                                     default=0)
    participation_rate = fields.Float(compute='_compute_participation_rate', string="Taux des participations",
                                      store=True, size=4)
    investment = fields.Integer("Total investissement")
    roi = fields.Integer("ROI")

    def _compute_participation_rate(self):
        for rec in self:
            if rec.nbr_coupon_util != 0:
                self.participation_rate = rec.coupon_count/rec.nbr_coupon_util

    def _calcule_nbr_coupon_util(self):
        for rec in self:
            s = rec.coupon_ids.search([('points', '=', 0), ('program_id', '=', rec.id)]).ids
            rec.nbr_coupon_util = int(len(s))
