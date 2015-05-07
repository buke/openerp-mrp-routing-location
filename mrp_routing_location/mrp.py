# -*- coding: utf-8 -*-
##############################################################################
#
#    mrp routing location
#    Copyright 2013 wangbuke <wangbuke@gmail.com>
#    Copyright 2015 credativ ltd. <ondrej.kuznik@credativ.co.uk>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models

class mrp_routing(models.Model):
    _inherit = 'mrp.routing'

    location_src_id = fields.Many2one('stock.location', 'Raw Materials Location',
                                      help="Location where the system will "
                                      "look for components.",)
    location_dest_id = fields.Many2one('stock.location', 'Finished Products Location',
                                      help="Location where the system will "
                                      "stock the finished products.",)


class mrp_production(models.Model):
    _inherit = 'mrp.production'

    @api.one
    def _src_id_default(self):
        if self.routing_id and self.routing_id.location_src_id:
            return self.routing_id.location_src_id.id
        return super(mrp_production, self)._src_id_default()

    @api.one
    def _dest_id_default(self):
        if self.routing_id and location_dest_id:
            return self.routing_id.location_dest_id.id
        return super(mrp_production, self)._dest_id_default()

    location_src_id = fields.Many2one('stock.location', 'Raw Materials Location',
                                      help="Location where the system will "
                                      "look for components.", default=_src_id_default)
    location_dest_id = fields.Many2one('stock.location', 'Finished Products Location',
                                      help="Location where the system will "
                                      "stock the finished products.",
                                      default=_dest_id_default)
    _default = {
            'location_src_id': _src_id_default,
    }

    def onchange_routing_id(self, cr, uid, ids, routing_id, context=None):
        if routing_id:
            routing = self.pool.get('mrp.routing').browse(cr, uid, routing_id, context=context)
            return {'value': {'location_src_id': routing.location_src_id.id, 'location_dest_id': routing.location_dest_id.id}}
        else:
            location_src_id = self._src_id_default(cr, uid, ids, context=context)
            location_dest_id = self._dest_id_default(cr, uid, ids, context=context)
            return {'value': {'location_src_id': location_src_id, 'location_dest_id':location_dest_id}}


class procurement_order(models.Model):
    _inherit = 'procurement.order'

    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        routing_model = self.pool.get('mrp.routing')

        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context=context)
        routing_id = res.get('routing_id')
        if routing_id:
            routing = routing_model.browse(cr, uid, routing_id, context=context)
            if routing.location_src_id:
                res['location_src_id'] = routing.location_src_id.id
            if routing.location_dest_id:
                res['location_dest_id'] = routing.location_dest_id.id
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
