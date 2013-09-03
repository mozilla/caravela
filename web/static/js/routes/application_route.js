App.ApplicationRoute = Em.Route.extend({
  model: function(){
    return this.get('store').find('insight');
  }
});
