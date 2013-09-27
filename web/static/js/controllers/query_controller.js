App.QueryController = Ember.ObjectController.extend({
  needs: ['application', 'insightTable'],

  query: "",

  execution_time: "0.0s",

  schema: Em.ArrayProxy.create({content:[]}),
  records: Em.ArrayProxy.create({content:[]}),


  saveDisabled: Ember.computed.not('isDirty'),



  url: function(){
    var query =  this.get('statement');

    if(query){
      return "/query?q=" + query;
    }
     
  }.property("statement"),

  execute_stmt: function(stmt){
    console.log('execute stmt');

    var self = this;
    var start = new Date().getTime();
    var self = this;
    self.set('execution_time', '0.0s');
    var timer = setInterval(function(){
      var elapsed = (new Date().getTime() - start) / 1000;
       self.set('execution_time', elapsed.toFixed(1) + 's');
    }, 50);
    
    var array = [];


    var url = '/query?q='+encodeURIComponent(stmt);

    console.log('clearing')
    this.get('records').clear();
    this.get('schema').clear();

    Ember.$.getJSON(url, function(json) {
      var schema = json.schema;
      var records = self.get('records');
      self.get('schema').addObjects(schema);
      
      json.records.forEach(function(record,i){
        var o = _.object(schema, record);

        records.addObject(Em.Object.create(o));
        //records.addObject(o)        
      });

    }).fail(function(){
      console.log('arguments', arguments)
      alert('failure');
    }).always(function(){
      clearInterval(timer);
    });

  },

  update: _.debounce(function(){
    console.log('update called');
    var query = this.get('statement');
    if(query){
      this.execute_stmt(query);
    }
  },300).observes('model'),


  actions:{
    execute: function(){
      console.log('execute called');

      this.update();
    },
    save: function(){
      this.get('model').save();
    }
  }


});

App.QueriesNewController = App.QueryController.extend({
  needs: ['insightTable'],
  name: null,
  statement: "",

  canSave: function(){
    return  Boolean(this.get('name') && this.get('statement'));
  }.property('name', 'statement'),


  actions:{
    save: function(){
      var query = this.get('store').createRecord(
        'query',
        this.getProperties('name', 'statement')
      );
      query.save();
      this.transitionToRoute('query', query);

    }
  }


});
