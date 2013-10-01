App.ApplicationController = Ember.ArrayController.extend({
  needs: ["insight", "user", "queries"],

  queries: Em.computed.alias("controllers.user.queries"),
  insights: Em.computed.alias("controllers.user.insights"),

  user: function(){
    return this.get('controllers.user');
  }.property()

});
