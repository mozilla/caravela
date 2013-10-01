App.ApplicationRoute = Em.Route.extend({
  model: function(){    
    this.controllerFor('queries').set(
      'content',
      this.get('store').find('query')
    );

  },

  actions:{
    error: function(error, transition){
      console.error(error.toString());
    },

    login: function(){
      this.controllerFor('user').login();
    },
    
    logout: function(){
      this.controllerFor('user').logout();
    }

  }
});
