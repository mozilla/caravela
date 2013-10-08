App.InsightRoute = Em.Route.extend({
  beforeModel: function(){
    var uc = this.controllerFor('user');
    if( !uc.get('content')){
      return new Em.RSVP.reject();
    }
  },

  actions:{
    error: function(reason, transition) {
      // Redirect to `login` but save the attempted Transition
      var loginController = this.controllerFor('user');
      loginController.set('afterLoginTransition', transition);
      this.transitionTo('index');
    }
  }


});
