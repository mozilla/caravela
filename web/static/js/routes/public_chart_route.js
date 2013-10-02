App.PublicChartRoute = Em.Route.extend({
  model: function(){
    return this.modelFor('public');
  },

  afterModel: function(insight){

    Em.run.later(null, function(){
      var query_controller = this.controllerFor('query');

      query_controller.set('model', insight.get('query'));
      query_controller.send('execute');

    }.bind(this),1000);
    return true;
  },



  renderTemplate: function(controller){
    this.render('insight.chart',
      {
        'controller': controller
      }
    );
  }
  
});