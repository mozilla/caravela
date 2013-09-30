window.App = Ember.Application.create({});


App.Router.map(function(){
  this.resource('insight', { path: ':insight_id' }, function(){
    this.route('chart');
    this.route('describe');
    this.route('comment');
  });

  this.resource('queries', { path: '/query' }, function(){
    this.route('new');
    this.resource('query', { path: ':query_id' });
  });

  

  this.route('views');
  this.route('schemas');
  this.route('functions');

});

App.ObjectTransform = DS.Transform.extend({
  deserialize: function(serialized) {
    return serialized;
  },
  serialize: function(deserialized) {
    return deserialized;
  }
});


App.FirebaseAdapter =  DS.Adapter.extend({
  baseRef: "https://caravela.firebaseio.com/",


  emptyPromise: function(result){
    // resolve immediatly we'll update the store
    // via push as the records come in
    result = result || {};
    return new Ember.RSVP.Promise(function(resolve, reject) {
      resolve(result);
    });

  },

  refForType: function(type){
    return new Firebase(this.get('baseRef')).child(
      Em.String.pluralize(type.typeKey)
    );
  },

  createRecord: function(store, type, record){

    var serializer = store.serializerFor(type.typeKey);
    var data = serializer.serialize(record, { includeId: true });

    var ref = this.refForType(type);   
    return new Ember.RSVP.Promise(function(resolve) {

      var childRef = ref.push(
        data
      );
      data.id = childRef.name();
      
      console.log("adding", type.typeKey, data)
      resolve(data);


    });

  },

  updateRecord: function(store, type, record){
    var serializer = store.serializerFor(type.typeKey);
    var data = serializer.serialize(record, { includeId: true });
    
    var ref = this.refForType(type).child(data.id);   
    return new Ember.RSVP.Promise(function(resolve,reject) {

      ref.set(
        data,
        function(err){
          if(err){
            reject(err);
          }else{
            resolve(data);
          }
        }
      );

    });

  },

  find: function(store, type, id){
    return this.emptyPromise({'id': id});
  },

  findAll: function(store, type){
    var ref = this.refForType(type);

    var controller = this;
    ref.on('child_added', function(snapshot){
      var record = snapshot.val();
      record.id = snapshot.name();

      // schedule in next loop so that if this was called because
      // of createRecord we preform an update rather than a creating
      // a duplicate.
      Em.run.next(null, function(){
        store.push(type, record);
      });        


    });

    /*
    ref.on('child_removed', function(snapshot){
      controller.removeItem(snapshot.name());
    });
    */

    ref.on('child_changed', function(snapshot){
      var record = snapshot.val();
      record.id = snapshot.name();
      store.push(type, record);

    });

    
    return this.emptyPromise();

  }
});


Ember.Table.RowArrayProxy.reopen({
  rowContent: function() {
    return []; 
  }.property('content.@each')
});