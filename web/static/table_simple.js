(function() {

  App.query = Ember.ObjectController.extend({
    limit: 100,
    columns: "",
    url: function(){
      var cols = this.get('columns');

      return "/json?limit=%@".fmt(this.get('limit')) +
        (cols ? "&cols=%@".fmt(cols):"");
      
    }.property("columns"),
    visualize_url: function(){
      return "/visualize" + encodeURI(this.get('url'));
    }.property("url")

  }).create();


  App.TableSimpleExample = Ember.Namespace.create();

  App.TableSimpleExample.LazyDataSource = Ember.ArrayProxy.extend({
  });

  App.TableSimpleExample.TableController = Ember.Table.TableController.extend({
    hasHeader: true,
    hasFooter: false,
    numFixedColumns: 0,
    numRows: 100,
    rowHeight: 30,
    urlBinding: "App.query.url",

    columns: function(key,value) {
      var self = this;
      
      if (_.isArray(value)){
        return value;
      }

      Ember.$.getJSON(this.get('url'), function(json) {
        var schema = json.schema;
        var columns = schema.map(function(name,index){

          return Ember.Table.ColumnDefinition.create({
            columnWidth: 220,
            headerCellName: name,
            contentPath: name
          });
        });

        self.set('columns', columns);
        var content = self.get("content.content")
        
        json.records.forEach(function(record,i){
          var row = content[i];
          schema.forEach(function(attr,j){
            row.set(attr, record[j]);
          })
          
        });

      });

      return [];
    }.property('url'),
    content: function() {
      return App.TableSimpleExample.LazyDataSource.create({
        content: _.range(this.get('numRows')).map(function(i){
          return Em.Object.create();
        })
      });
    }.property('numRows')
  });

}).call(this);
