App.InsightChartController = Em.ObjectController.extend({
  needs: ['insight',  'user',  'query'],
  thumbNail: '',

  execution_timeBinding: "controllers.query.execution_time",

  actions:{
    publish: function(){
      var user = this.get('controllers.user');
      var insight = this.get('model').getProperties(
        'id', 'name', 'description'
      );

      insight['thumbNail'] = this.get('thumbNail');
      insight['insight'] = this.get('model').serialize();
      insight['query'] = this.get('model.query').serialize();


      this.get('model').save();
      user.publishInsight(insight);
 
    },
    save: function(){
      this.get('model').save();
    }
  }
});
