App.QueriesNewRoute = Em.Route.extend({
  activate: function(){
    var controller = this.controllerFor('queries.new')
    var statement = controller.get('statement');
    if(statement){
      controller.send('execute')
    }
    return true;
  },
  deactivate: function(){
    var controller = this.controllerFor('queries.new');
    controller.setProperties({
      name:null,
      statement: ""
    });
    controller.get('records').clear();
    controller.get('schema').clear();
    return true;
  },


  renderTemplate: function(){
    this.render('query',
      {
        'controller': this.controllerFor('queries.new')
      }
    );
  }
})