App.QueryController = Ember.Controller.extend({
  needs: ['insight'],
  orderBy: null,
  where: null,
  columnsBinding: "controllers.insight.columns",
  limitBinding: "controllers.insight.limit",
  whereBinding: "controllers.insight.where",
  orderByBinding: "controllers.insight.order_by",


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

    var args = [];

    
    var limit =  this.get('limit') || 10;
    if(limit){
      args.push("limit=%@".fmt(limit));
    }

    var orderBy = this.get('orderBy');
    if(orderBy){
      args.push('order_by=%@'.fmt(orderBy));
    }

    var cols = this.get('columns');
    if(cols){
      args.push("cols=%@".fmt(cols));
    }

    var where = this.get('where');
    if(where){
      args.push("where=%@".fmt(where));
    }


    return "/json?" + args.join('&');
    
  }.property("columns", "limit", "orderBy", "where"),


  execute: _.debounce(function(){
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
