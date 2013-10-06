App.Insight = DS.Model.extend({
  content: DS.attr('string'),
  url: DS.attr('string'),
  name: DS.attr('string'),
  description: DS.attr('string'),
  
  query:  DS.belongsTo('query'),
  statement: Em.computed.alias('query.statement'),

  spec: function(){
    var spec;
    try{
      spec = JSON.parse(this.get('content'));
    }catch(e){
      spec = {}
    }

    return spec;
  }.property('content'),

/*
  statement: function(){
    var q = this.get('spec.query') || '';
    return q;
  }.property('spec'),
*/


  isTemp: function(){
    return this.get('id') == 'temp';
  }.property('id')

});


App.InsightAdapter = App.FirebaseAdapter.extend({
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

App.initializer({
  name: "loadInsight",
  initialize: function(container) {

    Ember.$.getJSON("/insights/temp", function(json) {
      var store = container.lookup('store:main');
      store.push('insight', json.insight);

    });
  }
});





