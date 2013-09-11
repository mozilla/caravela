App.InsightChartRoute = Em.Route.extend({
  model: function(){
    return this.modelFor("insight");
  },

  actions: {
    publish: function(){
      this.controller.send('publish');
    },
    save: function(){
      // route save from insight controller to 
      // the sub controller.
      this.controller.send('save');
    }
  }

});
