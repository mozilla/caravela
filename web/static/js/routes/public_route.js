App.PublicRoute = Em.Route.extend({
  model: function(params){
    return this.get('store').find('public_insight', params.public_insight_id);
  },
  
  renderTemplate: function(controller, transition){
    this.render('insight',
      {
        'controller':controller
      }
    );
  }
  
});