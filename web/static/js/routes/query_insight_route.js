App.QueryInsightRoute = Em.Route.extend({
  model: function(params, transition){

    return this.get('store')
      .find('insight', params.insight_id).then(null,function(){

        return this.get('store').find('publicInsight', params.insight_id);
      
      }.bind(this));

  }
  
});