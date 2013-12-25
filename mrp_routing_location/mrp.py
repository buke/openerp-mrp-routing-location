# -*- coding: utf-8 -*-
##############################################################################
#
#    mrp routing location
#    Copyright 2013 wangbuke <wangbuke@gmail.com>
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

from openerp.osv import osv, fields, orm

class mrp_routing(osv.osv):

    def _src_id_default(self, cr, uid, ids, context=None):
        try:
            location_model, location_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'stock_location_stock')
            self.pool.get('stock.location').check_access_rule(cr, uid, [location_id], 'read', context=context)
        except (orm.except_orm, ValueError):
            location_id = False
        return location_id

    def _dest_id_default(self, cr, uid, ids, context=None):
        try:
            location_model, location_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'stock_location_stock')
            self.pool.get('stock.location').check_access_rule(cr, uid, [location_id], 'read', context=context)
        except (orm.except_orm, ValueError):
            location_id = False
        return location_id

    _inherit = 'mrp.routing'
    _columns = {
        'location_src_id': fields.many2one('stock.location', 'Raw Materials Location', required=True,
            help="Location where the system will look for components."),
        'location_dest_id': fields.many2one('stock.location', 'Finished Products Location', required=True,
            help="Location where the system will stock the finished products."),
    }
    _defaults = {
        'location_src_id': _src_id_default,
        'location_dest_id': _dest_id_default
    }


class mrp_production(osv.osv):

    _inherit = 'mrp.production'
    def onchange_routing_id(self, cr, uid, ids, routing_id, context=None):
        if routing_id:
            routing = self.pool.get('mrp.routing').browse(cr, uid, routing_id, context=context)
            return {'value': {'location_src_id': routing.location_src_id.id, 'location_dest_id': routing.location_dest_id.id}}
        else:
            location_src_id = self._src_id_default(cr, uid, ids, context=context)
            location_dest_id = self._dest_id_default(cr, uid, ids, context=context)
            return {'value': {'location_src_id': location_src_id, 'location_dest_id':location_dest_id}}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
