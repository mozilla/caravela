App.IndexController = Ember.ArrayController.extend({
  needs: 'user',
  user: Em.computed.alias('controllers.user.content'),
  sortProperties: ['updated_at'],
  sortAscending: false,
  
  actions: {
    showInsight: function(pub_insight){
      var store = this.get('store');

      if(this.get('user.id') == pub_insight.get('user_id')){
        this.transitionToRoute(
          'insight.chart', 
          store.find('insight',pub_insight.id)
        );
      }else{
        this.transitionToRoute(
          'public.chart', 
          pub_insight
        );
      }
      
    }
  }
});
