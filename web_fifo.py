from openerp.osv import fields, orm

from fifo.api.wiggle import Wiggle

class web_fifo_server(orm.Model):
    '''FiFo server object, to store Wiggle access information'''
    _name = "web.fifo.server"
    _description = "Fifo Servers"
    _columns = {
        'name': fields.char('FiFo server name', size=50, required=True, help="Name of the FiFo server."),
        'active': fields.boolean('Active', help="The active field allows you to hide the FiFo server without deleting it."),
        'host': fields.char('FiFo host', size=50, required=True, help="IP address or hostname of the FiFo server."),
        'username': fields.char('FiFo username', size=30, required=True, help="Username that OpenERP will use for automated tasks."),
        'password': fields.char('FiFo password', size=30, required=True, help="Password that OpenERP will use for automated tasks."),
        'company_id': fields.many2one('res.company', 'Company', help="Company that uses the FiFo server."),
    }
    
    _defaults = {
        'active': True,
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'web.fifo.server', context=context),
    }
    
    def _get_fifo_server_from_user(self, cr, uid, context=None):
        '''Return a web.fifo.server browse object'''
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        if user.fifo_server_id.id:
            fifo_server = user.fifo_server_id
        else:
            fifo_server_ids = self.search(cr, uid, [('company_id', '=', user.company_id.id)], context=context)
            if not fifo_server_ids:
                raise orm.except_orm('Error:', "No FiFo server configured for the company '%s'." % user.company_id.name)
            else:
                fifo_server = self.browse(cr, uid, fifo_server_ids[0], context=context)
        return fifo_server

    def _connect_to_fifo(self, cr, uid, context=None):
        '''
        Open connection to Wiggle
        Returns an instance of Wiggle
        '''
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)

        fifo_server = self._get_fifo_server_from_user(cr, uid, context=context)

        if not user.fifo_username or not user.fifo_password:
            raise orm.except_orm('Error:', 'No FiFo details specified for the current user.')

        try:
            wiggle = Wiggle()
            wiggle.init(fifo_server.host, user.fifo_username, user.fifo_password, user.fifo_token)
            if wiggle.get_token():
                user.write({'fifo_token': wiggle.get_token()}, context=context)
        except Exception, e:
            raise orm.except_orm('Error in FiFo request:', str(e))
            return False

        return wiggle

class res_users(orm.Model):
    _inherit = "res.users"

    _columns = {
        'fifo_username': fields.char('FiFo username', size=30, help="The FiFo username for this user."),
        'fifo_password': fields.char('FiFo password', size=30, help="The FiFo password for this user."),
        'fifo_token': fields.char('FiFo token', size=50, help="The last token used for this user."),
        'fifo_server_id': fields.many2one('web.fifo.server', 'FiFo server', help="FiFo server that this user is on. If blank, the first in the company is used."),
    }
    
    def get_fifo_token(self, cr, uid, context=None):
        wiggle = self.pool['web.fifo.server']._connect_to_fifo(cr, uid, context)
        return wiggle.get_token()

class res_company(orm.Model):
    _inherit = "res.company"

    _columns = {
        'fifo_server_ids': fields.one2many('web.fifo.server', 'company_id', 'FiFo servers', help="List of FiFo servers.")
    }
