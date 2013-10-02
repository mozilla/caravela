App.PublicQuery = DS.Model.extend({
  name: DS.attr('string'),
  statement: DS.attr('string'),
  insight: DS.belongsTo('publicInsight')
});

App.PublicQueryAdapter = App.FirebaseAdapter.extend({
});
