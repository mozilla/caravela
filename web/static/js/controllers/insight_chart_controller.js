App.InsightChartController = Em.ObjectController.extend({
  needs: ['insight',  'user',  'query'],
  thumbNail: '',

  execution_timeBinding: "controllers.query.execution_time",

  modelActions: Em.ArrayProxy.create({content:[
    Em.Object.create({title: "Save", action: "save", icon: "icon-hdd" }),
    Em.Object.create({title: "Publish", action: "publish", icon: "icon-bullhorn" })
  ]}),


  actions:{
    dispatch: function(action){
      this.send(action)
    },

    publish: function(){
      var user = this.get('controllers.user');
      var insight = this.get('model').getProperties(
        'id', 'name', 'description', 'content'
      );

      insight['thumbNail'] = this.get('thumbNail');
      
      var query = this.get('model.query').serialize();
      delete query.insight;


      insight['query'] = query;

      this.get('model').save();
      user.publishInsight(insight);
      
      this.transitionToRoute('index');
 
    },
    save: function(){
      this.get('model').save();
    }
  }
});
