App.InsightTableController = Ember.Table.TableController.extend({
  hasHeader: true,
  hasFooter: false,
  numFixedColumns: 0,
  rowHeight: 30,

  needs: ["query"],

  columns: function(){
    var schema = this.get("controllers.query.schema");//Em.get("App.query.schema");

    if (!schema){
      return [];
    }else{
      return  schema.map(function(name,index){
        return Ember.Table.ColumnDefinition.create({
          columnWidth: 220,
          headerCellName: name,
          contentPath: name,
          sortAscending: false,
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
    //column.toggleProperty 'sortAscending'
    //@set 'sortColumn', column
    //@set 'sortAscending', column.get('sortAscending')

    column.toggleProperty('sortAscending');
    var direction = "DESC"
    if (column.get('sortAscending')){
      direction = "ASC"
    }

    this.set("controllers.query.orderBy", [
      column.get('contentPath'),
      direction
    ]);
   
    
  }

});

App.HeaderTreeCell = Ember.Table.HeaderCell.extend({
  templateName: 'table-header-tree-cell'  
});


