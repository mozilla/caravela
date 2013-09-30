App.ApplicationRoute = Em.Route.extend({
  model: function(){
    
    this.controllerFor('queries').set(
      'content',
      this.get('store').find('query')
    );

  },

  actions:{
    error: function(){
      alert('app error')
    }
  }
});
