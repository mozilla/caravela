App.InsightTableController = Ember.Table.TableController.extend({
  hasHeader: true,
  hasFooter: false,
  numFixedColumns: 0,
  //headerHeight: 30,
  rowHeight: 30,

  needs: ["query"],

  columns: function(){

    var schema = this.get("controllers.query.schema");//Em.get("App.query.schema");
    // TODO/BUG: this method fires off after sorting is complete
    // which resets the state of sortAscending back to true which
    if (!schema){
      console.log('columns!!!!!, no schema')
      return [];
    }else{
      console.log('columns!!!!!,with schema')
      return  schema.map(function(name,index){
        return Ember.Table.ColumnDefinition.create({
          columnWidth: 220,
          headerCellName: name,
          contentPath: name,

          //getCellContent: function(row){return row[name]},
          sortAscending: true,
          headerCellViewClass: 'App.HeaderTreeCell'
        });
      });
    }

  }.property("controllers.query.schema.@each"),


  content: Em.computed.alias("controllers.query.records"),

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


