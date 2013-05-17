(function() {

  window.App = Ember.Application.create({
  });


  App.ApplicationController = Ember.Controller.extend({
    tableController: Ember.computed(function() {
      return Ember.get('App.TableSimpleExample.TableController').create();
    }).property()
  });

}).call(this);
