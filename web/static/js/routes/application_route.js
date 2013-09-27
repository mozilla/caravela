App.ApplicationRoute = Em.Route.extend({
  model: function(){
    
    this.controllerFor('queries').set(
      'content',
      this.get('store').find('query')
    );


    return this.get('store').find('insight');
  }
});
