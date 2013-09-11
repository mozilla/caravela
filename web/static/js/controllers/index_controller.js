App.IndexController = Ember.ArrayController.extend({
  sortProperties: ['updated_at'],
  sortAscending: false,

  init:function(){
    this._super();
  
    var feedRef = new Firebase('https://caravela.firebaseio.com/feed')
                  .endAt()
                  .limit(10);
   
    var controller = this;

    feedRef.on('child_added', function(snapshot){
      var insight = snapshot.val();
      controller.addObject(snapshot.val());
    });

    feedRef.on('child_removed', function(snapshot){
      controller.removeItem(snapshot.name());
    });

    feedRef.on('child_changed', function(snapshot){
      controller.updateItem(snapshot.val());
    });

  },

  removeItem: function(id){
    var obj = this.findProperty("id", id);
    this.removeObject(obj);
  },

  updateItem: function(updates){
    var item = this.findProperty("id", updates.id);
    this.removeObject(item);
    this.addObject(updates);
  },

  actions: {
    showInsight: function(pub_insight){
      var insight = this.get('store').find('insight',pub_insight.id);
      this.transitionToRoute('insight.chart', insight);
    }
  }
});
