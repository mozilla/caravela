App.InsightChartView = Em.View.extend({
  classNames: ["chart"],

  thumbNailBinding: "controller.thumbNail",
  width:null,
  height: null,
  viz: null,
  specUpdated: function(){

    var spec   = this.get("controller.spec"),
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
      self.set('thumbNail', self.makeThumbNail());
    });



  }.observes("controller.spec", "controller.controllers.query.records.@each"),

  didInsertElement: function(){
    this.specUpdated();
  },

  makeThumbNail: function(){
    var canvas = this.$("canvas")[0];
    return canvas.toDataURL("image/png");
  }


});
