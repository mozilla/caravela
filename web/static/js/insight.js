App.InsightController = Em.ObjectController.extend({
  needs: "query"
});

App.Insight = DS.Model.extend({

  content: DS.attr('string'),
  
  spec: function(){
    var spec;
    try{
      spec = JSON.parse(this.get('content'));
    }catch(e){
      spec = {}
    }

    return spec;
  }.property('content'),

  columns: function(){
    return this.get('spec.columns');
  }.property('spec'),

  order_by: function(){
    return this.get('spec.order_by') || '';
  }.property('spec'),

  limit: function(){
    return this.get('spec.limit');
  }.property('spec'),

  where: function(){
    return this.get('spec.where');
  }.property('spec'),




  name: function(){
    return this.get('spec.name');
  }.property('spec'),

  isTemp: function(){
    return this.get('id') == 'temp';
  }.property('id')

});

App.Insight.FIXTURES = [{
  id: 1,
  name: "Google Analytics"
},{
  id: 2,
  name: "Size Histogram"
}]