App.QueryController = Ember.Controller.extend({
  needs: ['application', 'insightTable'],

  query: "",

  execution_time: "0.0s",
  

  _schema: Em.ArrayProxy.create({content:[]}),
  _records: Em.ArrayProxy.create({content:[]}),


  schema: function(){
    this.send('execute');
    return this._schema;
  }.property(),

  records: function(){
    this.send('execute');
    return this._records;
  }.property(),


  url: function(){
    console.log('query change', query)
    var query =  this.get('query');

    if(query){
      return "/query?q=" + query;
    }
     
  }.property("query"),

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

    var url = '/query?q='+encodeURIComponent(stmt);


    Ember.$.getJSON(url, function(json) {
      var schema = json.schema;
      var array = [];

      self.set('_schema.content', schema);
      
      json.records.forEach(function(record,i){
        var o = _.object(schema, record);

        array.push(Em.Object.create(o));          
      });

      self.set('_records.content', array);

    }).fail(function(){
      console.log('arguments', arguments)
      alert('failure');
    }).always(function(){
      clearInterval(timer);
    });

  },

  update: _.debounce(function(){
      var query = this.get('query');
      if(query){
        this.execute_stmt(query);
      }
  },300).observes('query'),

  actions:{
    execute: function(){
      this.update();
    }
  }


});
