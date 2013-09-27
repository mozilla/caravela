App.QueriesNewRoute = Em.Route.extend({

  renderTemplate: function(){
    this.render('query',
      {
        'controller': this.controllerFor('queries.new')
      }
    );
  }
})