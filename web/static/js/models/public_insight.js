App.PublicInsight = DS.Model.extend({
  name: DS.attr('string'),
  description: DS.attr('string'),
  thumbNail: DS.attr('string'),
  content: DS.attr('string'),

  user_id: DS.attr('string'),
  nickname: DS.attr('string'),
  avatar_url: DS.attr('string'),
 
  updated_at: DS.attr('number'),
  url: DS.attr('string'),

  query:  DS.belongsTo('publicQuery'),

  spec: function(){
    var spec;
    try{
      spec = JSON.parse(this.get('content'));
    }catch(e){
      spec = {}
    }

    return spec;
  }.property('content'),

});


App.PublicInsightAdapter = App.FirebaseAdapter.extend({
  refForType:  function(type){
    return new Firebase(this.get('baseRef')).child('feed');
      //.endAt()
      //.limit(10);
  }
});



App.PublicInsightSerializer = DS.JSONSerializer.extend({
  
  extractSingle: function(store, type, payload, id, requestType) {
    
    if(payload.query){
      var query = payload.query;
      payload.query = id;
      query.id = id;
      query.insight = id;
      store.push('publicQuery', query);
    }

    return this._super(store, type, payload, id, requestType);    
  }
});

