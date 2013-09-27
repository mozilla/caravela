App.InsightRoute = Em.Route.extend({
  setupController: function(controller, model){
    this._super(controller, model);

    this.controllerFor('query').set('model', model.get('query'));
  }

});
