window.App = Ember.Application.create({});


App.Router.map(function(){
  this.resource('insight', { path: ':insight_id' }, function(){
    this.route('table');
    this.route('chart');
    this.route('spec');
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
