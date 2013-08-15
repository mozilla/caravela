App.QueryController = Ember.Controller.extend({
  needs: ['insight'],

  queryBinding: "controllers.insight.query",
  execution_time: "0.0s",
  

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
    var query =  this.get('query');
    if(query){
      return "/query?q=" + query;
    }
     
  }.property("controllers.insight.model"),

  execute_stmt: function(stmt){
    var self = this;
    var start = new Date().getTime();
    var self = this;
    self.set('execution_time', '0.0s');
    var timer = setInterval(function(){
      var elapsed = (new Date().getTime() - start) / 1000;
       self.set('execution_time', elapsed.toFixed(1) + 's');
    }, 50);
    
    var array = [];
    self.set('_records.content', []);

    Ember.$.getJSON('/query?q='+stmt, function(json) {
      var schema = json.schema;
      var array = [];

      self.set('_schema.content', schema);
      
      json.records.forEach(function(record,i){
        var o = _.object(schema, record);

        array.push(Em.Object.create(o));          
      });

      self.set('_records.content', array);

    }).fail(function(){
      alert('failure');
    }).always(function(){
      clearInterval(timer);
    });

  },

 
  execute: _.debounce(function(){
    var query = this.get('query');
    if(query){
      this.execute_stmt(query);
    }
  },300).observes('url')


});
