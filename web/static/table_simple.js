App.InsightTableController = Ember.Table.TableController.extend({
  hasHeader: true,
  hasFooter: false,
  numFixedColumns: 0,
  rowHeight: 30,

  needs: ["query"],

  columns: function(){
    var schema = this.get("controllers.query.schema");//Em.get("App.query.schema");
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
          sortAscending: true,
          headerCellViewClass: 'App.HeaderTreeCell'
        });
      });
    }

  }.property("controllers.query.schema.@each"),


  // TODO: figure out why we can't bind the table controller
  // directly to to array controller with a binding such as
  // contentBinding:  Ember.Binding.oneWay("App.query"),
  content: function(k,v){
    var records = this.get("controllers.query.records");
    return records;
  }.property("controllers.query.records.@each"),


  sortByColumn: function(column){
    column.toggleProperty('sortAscending');

    var direction = "ASC"
    if (column.get('sortAscending') == false){
      direction = "DESC"
    }

    this.set("controllers.query.orderBy", [
      column.get('contentPath') + ' ' +direction
    ]);
   
    
  }

});

App.HeaderTreeCell = Ember.Table.HeaderCell.extend({
  templateName: 'table-header-tree-cell'  
});


