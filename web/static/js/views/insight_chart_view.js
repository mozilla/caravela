App.InsightChartView = Em.View.extend({
  classNames: ["chart"],

  thumbNailBinding: "controller.thumbNail",
  width:null,
  height: null,
  viz: null,
  updateProps: ["controller.spec", "controller.controllers.query.records.@each"],

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



  },

  didInsertElement: function(){
    //.observes("controller.spec", "controller.controllers.query.records")
    this.get('updateProps').forEach(function(p){
      this.addObserver(p, this, this.specUpdated)
    }.bind(this));
    this.specUpdated();
  },

  willDestroyElement: function(){
    this.get('updateProps').forEach(function(p){
      this.removeObserver(p, this, this.specUpdated)
    }.bind(this));
  },


  makeThumbNail: function(){
    var canvas = this.$("canvas");
    if(canvas && canvas.length){
      return canvas[0].toDataURL("image/png");
    }
  }


});
