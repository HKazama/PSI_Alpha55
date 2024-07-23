# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class LoyaltyProgram(models.Model):
    """To set the point rate when change is converted to loyalty points"""
    _inherit = 'loyalty.program'

    nbr_coupon_util = fields.Integer(string='Nombre de coupons utilisés', compute="_calcule_nbr_coupon_util",
                                     default=0)
    participation_rate = fields.Float(compute='_compute_participation_rate', string="Taux des participations",
                                      default=0, size=4)
    investment = fields.Integer("Total investissement")
    roi = fields.Float("ROI", compute='_compute_roi', size=6)
    total_order = fields.Float("Total payer par programme", compute='_compute_total_order')

    def _compute_roi(self):
        for rec in self:
            if rec.investment != 0:
                rec.roi = (rec.total_order - rec.investment) / rec.investment
            else:
                rec.roi = 0.0

    def _compute_total_order(self):
        for rec in self:
            total = 0.0

            coupon = rec.coupon_ids.search([('points', '=', 0), ('program_id', '=', rec.id)])
            for order in coupon:
                total += order.source_pos_order_id.amount_paid
            rec.total_order = total

    def _compute_participation_rate(self):
        for rec in self:
            if rec.coupon_count != 0:
                rec.participation_rate = rec.nbr_coupon_util/rec.coupon_count
            else:
                rec.participation_rate = 0.0

    def _calcule_nbr_coupon_util(self):
        for rec in self:
            s = rec.coupon_ids.search([('points', '=', 0), ('program_id', '=', rec.id)]).ids
            rec.nbr_coupon_util = int(len(s))
