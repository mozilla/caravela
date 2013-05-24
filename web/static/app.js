window.App = Ember.Application.create({});

App.Store = DS.Store.extend({
  revision: 12,
});

App.Router.map(function(){
  this.resource('insight', { path: ':insight_id' }, function(){
    this.route('table');
    this.route('chart');
    this.route('spec');

  });
});

App.ApplicationRoute = Em.Route.extend({
  model: function(){
    return App.Insight.find();
  }
});

App.IndexRoute = Em.Route.extend({
  model: function(){
    return App.Insight.find("temp");
  },
  redirect: function(model){
    this.transitionTo("insight.table", model);
  }
});

App.InsightChartRoute = Em.Route.extend({
  model: function(){
    return this.controllerFor('insight');
  }
});

App.ApplicationController = Ember.ArrayController.extend({
  needs: "insight",
  save: function(){
    var props = App.query.getProperties('columns', 'spec');
  }
});
