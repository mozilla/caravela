App.PublicChartController = Em.ObjectController.extend({
  needs:['query'],

  execution_timeBinding: "controllers.query.execution_time",

  modelActions: Em.ArrayProxy.create({content:[
    Em.Object.create({title: "Fork", action: "fork", icon: "icon-fork" })
  ]}),

  spec: function(){
    return JSON.parse(this.get('model.content'))
  }.property('model.content'),

  actions: {
    dispatch: function(action){
      this.send(action)
    },
    fork: function(){
      
      var i = this.get('model').serialize(),
          q = this.get('model.query').serialize();

      delete i.query;
      delete q.insight;

      var insight = this.get('store').createRecord('insight', i),
          query = this.get('store').createRecord('query',q);

      var self = this;

      query.save().then(function(){
        insight.set('query', query);
        insight.save().then(function(){
          query.set('insight', insight);
          query.save();
          self.transitionToRoute('insight.chart', insight);
        });
      });

    }

  }
});