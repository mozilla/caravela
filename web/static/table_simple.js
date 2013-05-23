(function() {

  App.TableController = Ember.Table.TableController.extend({
    hasHeader: true,
    hasFooter: false,
    numFixedColumns: 0,
    rowHeight: 30,

    columns: function(){
      var schema = Em.get("App.query.schema");
      
      if (!schema){
        return [];
      }else{
        return  schema.map(function(name,index){
          return Ember.Table.ColumnDefinition.create({
            columnWidth: 220,
            headerCellName: name,
            contentPath: name
          });
        });
      }

    }.property("App.query.schema"),

  
    // TODO: figure out why we can't bind the table controller
    // directly to to array controller with a binding such as
    // contentBinding:  Ember.Binding.oneWay("App.query"),
    content: function(k,v){
      return Em.get("App.query");
    }.property("App.query.content"),

   
  
  });

}).call(this);
