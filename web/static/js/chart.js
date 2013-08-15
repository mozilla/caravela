App.InsightChartController = Em.ObjectController.extend({
  needs: ['insight', 'query'],
 
});

App.InsightChartView = Em.View.extend({
  classNames: ["Chart", "well"],
  viz: null,
  specUpdated: function(){
 
    var spec   = this.get("controller.model.spec"),
        element = this.get("element"),
        documents = this.get("controller.controllers.query.records");

    if(!spec || !element || !documents) return;

    var self = this;    
    vg.parse.spec(spec, function(chart) {
      var viz = chart({el:element});

      self.set('viz', viz);

      
      viz.data({
        "documents": documents
      });
      

      viz.update();
    });

  }.observes("controller.model.spec", "controller.controllers.query.records.@each"),

  didInsertElement: function(){
    this.specUpdated();
  }


});
