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
      
      var i = this.get('model').serialize();
      i.query = this.get('model.query');

      var insight = this.get('store').createRecord('insight', i);

      insight.save().then(function(){
        this.transitionToRoute('insight.chart', insight);
      }.bind(this));


    }

  }
});