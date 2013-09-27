App.SchemasController = Ember.ArrayController.extend({
  //needs: ['query'],

  actions:{
    toggleSchema: function(schema){
      schema.toggleProperty('showSchema');
    },
    query: function(schema){
      var stmt = "select * from %@ limit 10".fmt(schema.get('name'));
      var query_controller = this.get('controllers.query');
      query_controller.set('query', stmt);
      this.transitionToRoute('query');
    }
  }
});