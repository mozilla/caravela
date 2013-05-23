(function() {

  window.App = Ember.Application.create({});

  App.Store = DS.Store.extend({
    revision: 12,
  });

  App.Router.map(function(){
    this.route('table');
    this.route('chart');
    this.route('spec');
  });

  App.ApplicationRoute = Em.Route.extend({
    model: function(){
      return App.Insight.find();
    }
  });

  App.IndexRoute = Em.Route.extend({
    redirect: function(){
      this.transitionTo("table");
    }
  });

  App.ChartRoute = Em.Route.extend({
    model: function(){
      return Em.get('App.query')
    }
  });

  App.SpecRoute = Em.Route.extend({
    model: function(){
      return Em.get('App.query')
    }
  });

  App.ApplicationController = Ember.ArrayController.extend({
    save: function(){
      var props = App.query.getProperties('columns', 'spec');

    }
  });

  App.query = Ember.ArrayController.extend({
    limit: 10,
    columns: "",

    columnWatcher: _.debounce(function(){
      this.fetch();
    },300).observes('columns'),

    url: function(){
      var cols = this.get('columns');
      return "/json?limit=%@".fmt(this.get('limit')) +
        (cols ? "&cols=%@".fmt(cols):"");
      
    }.property("columns"),

    fetch: function(){
      var self = this;
      var array = [];
      Ember.$.getJSON(this.get('url'), function(json) {
        var schema = json.schema;
        self.set('schema', schema);
        
        json.records.forEach(function(record,i){
          var o = _.object(schema, record);
          array.push(Em.Object.create(o));          
        });

        self.set('content', array);
      });
      return array;
    },


    spec: function(key, value){
      if(arguments.length == 2){
        return value;
      }

      var self = this;
      $.ajax({
        dataType: "text",
        url: '/spec/',
        success: function(data){
          self.set('spec', data);
        }
      });
    }.property()

  }).create();
  App.query.fetch();




}).call(this);
