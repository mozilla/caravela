App.InsightController = Em.ObjectController.extend({
  needs: "query"
});

App.Insight = DS.Model.extend({

  limit: DS.attr('number', {defaultValue:10}),
  content: DS.attr('string'),
  
  spec: function(){
    return JSON.parse(this.get('content'));
  }.property('content'),

  columns: function(){
    return this.get('spec.columns');
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