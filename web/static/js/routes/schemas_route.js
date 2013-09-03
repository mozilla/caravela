App.SchemasRoute = Em.Route.extend({
  //setupController: function(controller){
  //  controller.set('model',  App.Schema.all());
  //}
  model: function(){
    return this.get('store').find('schema');
  }
});
