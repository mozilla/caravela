App.InsightChartController = Em.ObjectController.extend({
  needs: ['insight', 'query', 'user'],
  thumbNail: '',

  actions:{
    publish: function(){
      var user = this.get('controllers.user');
      var insight = this.get('model').getProperties(
        'id', 'name', 'description'
      );

      insight['thumbNail'] = this.get('thumbNail');
      user.publishInsight(insight);
 
    },
    save: function(){}
  }
});
