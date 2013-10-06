App.Query = DS.Model.extend({
  name: DS.attr('string'),
  statement: DS.attr('string'),
  insight: DS.belongsTo('insight')
});



App.QueryAdapter = App.FirebaseAdapter.extend({
  /*
  refForType: function(type){
    var user_id = App.__container__.lookup('controller:user').get('id');
    return new Firebase(this.get('baseRef')).child(
      "users/%@/%@".fmt(
        user_id,
        Em.String.pluralize(type.typeKey)
      ) 
    );
  }
  */
});
