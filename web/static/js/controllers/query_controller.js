
App.QueryController = Ember.Table.TableController.extend({
  needs: ['application', 'insightTable'],

  hasHeader: true,
  hasFooter: false,
  numFixedColumns: 0,
  //headerHeight: 30,
  rowHeight: 30,

  query: "",

  execution_time: "0.0s",

  schema: Em.ArrayProxy.create({content:[]}),
  records: Em.ArrayProxy.create({content:[]}),


  saveDisabled: Ember.computed.not('isDirty'),

  visualizeDisabled: Em.computed.none('insight'),


  //bodyContent: Em.computed.alias("records"),

  bodyContent:  function(){
    return Ember.Table.RowArrayProxy.create({
      tableRowClass: Ember.Table.Row,
      content: this.get('records')
    });
  }.property('records'),

  isDirty: Em.computed.alias("model.isDirty"),
  name: Em.computed.alias("model.name"),
  statement: Em.computed.alias("model.statement"),
  insight: Em.computed.alias("model.insight"),


  columns: function(){

    var schema = this.get("schema");//Em.get("App.query.schema");
    // TODO/BUG: this method fires off after sorting is complete
    // which resets the state of sortAscending back to true which
    if (!schema){
      return [];
    }else{
      return  schema.map(function(name,index){
        return Ember.Table.ColumnDefinition.create({
          columnWidth: 220,
          headerCellName: name,
          contentPath: name,

          /*getCellContent: function(row){
            return row[name]
          },*/
          sortAscending: true,
          headerCellViewClass: 'App.HeaderTreeCell'
        });
      });
    }

  }.property("schema.@each"),



  url: function(){
    var query =  this.get('statement');

    if(query){
      return "/query?q=" + query;
    }
     
  }.property("statement"),

  execute_stmt: function(stmt){
    var self = this;
    var start = new Date().getTime();
    var self = this;

    if (self.timer){
      clearInterval(self.timer);
    }
    self.set('execution_time', '0.0s');


    var timer;
    timer = self.timer = setInterval(function(){
      var elapsed = (new Date().getTime() - start) / 1000;
       self.set('execution_time', elapsed.toFixed(1) + 's');
    }, 50);
    
    var array = [];


    var url = '/query?q='+encodeURIComponent(stmt);

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
      alert('failure');
    }).always(function(){
      clearInterval(timer);
    });

  },

  update: _.debounce(function(){
    var query = this.get('statement');
    if(query){
      this.execute_stmt(query);
    }
  },300).observes('model'),


  actions:{
    execute: function(){
      this.update();
    },
    save: function(){
      this.get('model').save();
    },
    visualize: function(){
      this.transitionToRoute('insight.chart', this.get('insight'));

    }
  }


});


/* QueriesNewController defined here because it
   inherits from QueryController 
*/
App.QueriesNewController = App.QueryController.extend({
  needs: ['insightTable'],
  name: null,
  statement: "",

  schema: Em.ArrayProxy.create({content:[]}),
  records: Em.ArrayProxy.create({content:[]}),

  saveDisabled:  function(){
    return  !Boolean(this.get('name') && this.get('statement'));
  }.property('name', 'statement'),

  visualizeDisabled: Em.computed.alias('saveDisabled'),

  newQuery:function(){
    var query = this.get('store').createRecord(
      'query',
      this.getProperties('name', 'statement')
    );
    return query.save();
  },

  actions:{
    save: function(){
      this.transitionToRoute('query', this.newQuery());
    },

    visualize: function(){
      var store = this.get('store'),
        self = this,
        statement =  this.get('statement');

      var query = this.newQuery();
      var temp  = store.find('insight','temp');

      Ember.RSVP.all([query, temp]).then(function(records){
        query = records[0],
        temp = records[1];

        var spec = temp.get('spec') || {};
        spec.query = statement;
        spec.name = '%@ Visual'.fmt(query.get('name'));

        var insight =  store.createRecord('insight', {
          name: spec.name, 
          content:JSON.stringify(spec, null, "  "),
          query:query
        });

        return insight.save().then(function(){
          query.set('insight', insight);
          query.save();
          self.transitionToRoute('insight.chart', insight);
        });

      }) 

    }
  }


});
