App.ChartController = Em.ObjectController.extend({
});

App.ChartView = Em.View.extend({
  classNames: ["Chart", "well"],
  viz: null,
  specUpdated: function(){

    var spec   = this.get("controller.spec"),
        element = this.get("element"),
        documents = this.get("controller.model.content") || {};


    if(!spec || !element ) return;

    spec = JSON.parse(spec);

    var self = this;    
    vg.parse.spec(spec, function(chart) {
      var viz = chart({el:element});

      self.set('viz', viz);

      
      viz.data({
        "documents": documents
      });
      

      viz.update();
    });

  }.observes("controller.spec"),

  didInsertElement: function(){
    this.specUpdated();
  }


});
