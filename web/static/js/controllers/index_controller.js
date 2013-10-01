App.IndexController = Ember.ArrayController.extend({
  needs: 'user',
  user: Em.computed.alias('controllers.user.content'),
  sortProperties: ['updated_at'],
  sortAscending: false,
  
  actions: {
    showInsight: function(pub_insight){
      var insight,
          store = this.get('store');

      if(this.get('user.id') == pub_insight.get('user_id')){
        insight = store.find('insight',pub_insight.id);        
      }else{
        var insight = Em.Object.create(pub_insight.get('insight'));
        var query = Em.Object.create(pub_insight.get('query'));


        insight.setProperties({
          'query':query,
          'name': pub_insight.get('name'),
          'description': pub_insight.get('description'),
          'spec': JSON.parse(insight.get('content'))
        });
        
        query.set('insight', insight);

        /*
        insight = store.createRecord('insight', rec);
        rec = pub_insight.get('query');
        delete rec['insight'];
        query = store.createRecord('query', rec);

        // Ember Data docs claim inverse shouldn't need to be 
        // set, but I encoutre bugs if I do not
        insight.set('query', query);
        query.set('insight', insight)
        */
      }
 
      this.transitionToRoute('insight.chart', insight);
    }
  }
});
