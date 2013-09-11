window.App = Ember.Application.create({});


App.Router.map(function(){
  this.resource('insight', { path: ':insight_id' }, function(){
    this.route('chart');
    this.route('describe');
    this.route('comment');
  });

  this.route('query');
  this.route('views');
  this.route('schemas');
  this.route('functions');

});

App.ObjectTransform = DS.Transform.extend({
  deserialize: function(serialized) {
    return serialized;
  },
  serialize: function(deserialized) {
    return deserialized;
  }
});
