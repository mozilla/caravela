App.InsightChartRoute = Em.Route.extend({
  model: function(){
    return this.modelFor("insight");
  },

  afterModel: function(insight){

    Em.run.later(null, function(){
      var query_controller = this.controllerFor('query');

      query_controller.set('model', insight.get('query'));
      query_controller.send('execute');

    }.bind(this),1000);
    return true;
  },

  actions: {
    publish: function(){
      this.controller.send('publish');
    },
    save: function(){
      // route save from insight controller to 
      // the sub controller.
      this.controller.send('save');
    }
  }

});
