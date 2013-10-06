App.MyQuery = DS.Model.extend({
  query: DS.belongsTo('query')
});

App.MyQueryAdapter = App.FirebaseAdapter.extend({
  refForType: function(type){
    var user_id = App.__container__.lookup('controller:user').get('id');
    return new Firebase(this.get('baseRef')).child(
      "users/%@/%@".fmt(
        user_id,
        Em.String.pluralize(type.typeKey)
      ) 
    );
  }
});
