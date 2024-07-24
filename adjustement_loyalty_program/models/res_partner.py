# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression
import dateutil.parser



class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_count_new = fields.Integer("Total des ventes", readonly=1)
    pos_order_count_new = fields.Integer("Total des points de ventes",  readonly=1)
    total_total = fields.Integer("Total", compute='_compute_total_total', store=True)
    total_total_dh = fields.Integer("Total des ventes en dh", compute='_compute_total_total', store=True)
    all_loyalty_card_count = fields.Integer(compute='_compute_all_loyalty_card',  store=True)
    loyalty_nbr = fields.Integer(compute='_compute_all_loyalty_card',  store=True)
    participation_rate = fields.Float(compute='_compute_participation_rate', store=True, size=4)
    create_date = fields.Datetime(readonly=False)

    @api.depends('sale_order_count_new', 'pos_order_count_new')
    def _compute_total_total(self):
        for rec in self:
            total_pos_sale = 0.0
            self.total_total = rec.sale_order_count_new + rec.pos_order_count_new
            for total in rec.pos_order_ids:
                total_pos_sale += total.amount_total
            for total in rec.sale_order_ids:
                total_pos_sale += total.amount_total
            rec.total_total_dh = total_pos_sale


    def _compute_pos_order(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search_fetch(
            [('id', 'child_of', self.ids)],
            ['parent_id'],
        )
        pos_order_data = self.env['pos.order']._read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            groupby=['partner_id'], aggregates=['__count']
        )
        self_ids = set(self._ids)

        self.pos_order_count = 0
        self.pos_order_count_new = 0
        for partner, count in pos_order_data:
            while partner:
                if partner.id in self_ids:
                    partner.pos_order_count += count
                    partner.pos_order_count_new += count
                partner = partner.parent_id

    def _compute_sale_order_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search_fetch(
            [('id', 'child_of', self.ids)],
            ['parent_id'],
        )
        sale_order_groups = self.env['sale.order']._read_group(
            domain=expression.AND([self._get_sale_order_domain_count(), [('partner_id', 'in', all_partners.ids)]]),
            groupby=['partner_id'], aggregates=['__count']
        )
        self_ids = set(self._ids)

        self.sale_order_count = 0
        self.sale_order_count_new = 0
        for partner, count in sale_order_groups:
            while partner:
                if partner.id in self_ids:
                    partner.sale_order_count += count
                    partner.sale_order_count_new += count
                partner = partner.parent_id

    def _compute_participation_rate(self):
        for rec in self:
            if rec.loyalty_nbr != 0 :
                self.participation_rate = rec.all_loyalty_card_count/rec.loyalty_nbr

    @api.depends('loyalty_card_count')
    def _compute_all_loyalty_card(self):
        for rec in self:
            all_loyalty_card_count = self.env['loyalty.card'].search([('partner_id', '=', rec.id),
                                                                      ('points', '=', 0)]).ids
            loyalty_nbr = self.env['loyalty.card'].search([('partner_id', '=', rec.id)]).ids
            if all_loyalty_card_count:
                self.loyalty_nbr = int(len(all_loyalty_card_count))
            if loyalty_nbr:
                self.all_loyalty_card_count = int(len(loyalty_nbr))
