App.Query = DS.Model.extend({
  name: DS.attr('string'),
  statement: DS.attr('string'),
  insight: DS.belongsTo('insight'),
  ownerId: DS.attr('string')
});


App.QueryAdapter = App.FirebaseAdapter.extend({});