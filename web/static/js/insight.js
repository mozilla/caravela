App.Insight = DS.Model.extend({
  name: DS.attr("string"),
  columns: DS.attr('string'),
  limit: DS.attr('number'),
  spec: DS.attr('string')
});

App.Insight.FIXTURES = [{
  id: 1,
  name: "Google Analytics"
},{
  id: 2,
  name: "Size Histogram"
}]