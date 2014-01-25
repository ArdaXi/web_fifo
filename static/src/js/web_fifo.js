openerp.web_fifo = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t,
        _lt = instance.web._lt;
        
    console.log("fifo loaded");
    
    instance.web_fifo.machines = instance.web.Widget.extend({
        start: function() {
            var Users = new instance.web.Model('res.users');
            Users.call('call_fifo', ['Package', 'list']).then(function (result) { console.log(result); });
            this.$el.text("Hello, world!");
            return this._super();
        },
    });
    
    instance.web.client_actions.add('web_fifo.machines', 'instance.web_fifo.machines');
}