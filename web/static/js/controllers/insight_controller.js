
App.InsightController = Em.ObjectController.extend({
  needs: ["query"],
  updateQuery: function(ob,key){
    this.set('controllers.query.query', ob.get(key))
  }.observes('query')
});
