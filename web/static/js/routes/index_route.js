App.IndexRoute = Em.Route.extend({
  model: function(){
    return this.get('store').find('publicInsight');
  }

});
