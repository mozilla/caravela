App.QueryController = Ember.Controller.extend({
  needs: ['insight'],

  columnsBinding: "controllers.insight.columns",
  limitBinding: "controllers.insight.limit",

  _schema: Em.ArrayProxy.create({content:[]}),
  _records: Em.ArrayProxy.create({content:[]}),

  schema: function(){
    this.execute();
    return this._schema;
  }.property(),

  records: function(){
    this.execute();
    return this._records;
  }.property(),


  url: function(){
    var cols = this.get('columns');
    return "/json?limit=%@".fmt(this.get('limit')) +
      (cols ? "&cols=%@".fmt(cols):"");
    
  }.property("columns"),


  execute: _.debounce(function(){
  console.log(this.get('columns'));

    var self = this;
    var array = [];
    Ember.$.getJSON(this.get('url'), function(json) {
      var schema = json.schema;

      self.set('_schema.content', schema);
      
      json.records.forEach(function(record,i){
        var o = _.object(schema, record);
        array.push(Em.Object.create(o));          
      });

      self.set('_records.content', array);
    });
    return self;
  },300).observes('url')

});
