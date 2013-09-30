App.SchemasController = Ember.ArrayController.extend({
  needs: ['queries_new'],

  actions:{
    toggleSchema: function(schema){
      schema.toggleProperty('showSchema');
    },

    query: function(schema){
      var stmt = "select * from %@ limit 10".fmt(schema.get('name'));
      var query_controller = this.get('controllers.queries_new');
      query_controller.set('statement', stmt);
      this.transitionToRoute('queries.new');
    }
  }
});