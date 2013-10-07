window.App = Ember.Application.create({});


App.Router.map(function(){
  this.resource('insight', { path: ':insight_id' }, function(){
    this.route('chart');
    this.route('describe');
    this.route('comment');
  });

  this.resource('public', { path: 'public/:public_insight_id' }, function(){
    this.route('chart');
    this.route('query');
    this.route('describe');
  });

  this.resource('queries', { path: '/query' }, function(){
    this.route('new');
    this.resource('query', { path: ':query_id' }, function(){
      this.route('insight', { path: ':insight_id' });
    });
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
  willDestroy: function(){
    new Firebase(this.get('baseRef')).off();
  },


  emptyPromise: function(result){
    // resolve immediatly we'll update the store
    // via push as the records come in
    
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
      data.url = childRef.toString();
      console.log("adding", type.typeKey, data)
      resolve(data);


    });

  },

  deleteRecord: function(store, type, record){
    return this.emptyPromise();
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

    return new Ember.RSVP.Promise(function(resolve, reject) {
      var ref = this.refForType(type);
      ref.child(id).once('value', function(snapshot){
        var record = snapshot.val();// || {id:id};
        if(record){
          resolve(record);          
        }else{
          reject('%@ not found'.fmt(id));
        }

      })

    }.bind(this))

  },

  findAll: function(store, type){
    var ref = this.refForType(type);
    var serializer = store.serializerFor(type);
    var controller = this;
    ref.on('child_added', function(snapshot){
      var record = snapshot.val();
      record.id = snapshot.name();
      record.url = snapshot.ref().toString();

      // schedule in next loop so that if this was called because
      // of createRecord we preform an update rather than a creating
      // a duplicate.

      Em.run.next(null, function(){
        out = serializer.extractSingle(store, type, record, record.id, 'find');
        store.push(type, out);          
      });        


    });

    
    ref.on('child_removed', function(snapshot){

      var id = snapshot.name();
      console.log('removing', type,id)
      var record = store.recordForId(type, id);
      record.unloadRecord();
    });
    

    ref.on('child_changed', function(snapshot){
      var record = snapshot.val();
      record.id = snapshot.name();
      record.url = snapshot.ref().toString();
      out = serializer.extractSingle(store, type, record, record.id, 'find');

      store.push(type, out);        

    });

    
    return this.emptyPromise([]);

  }

});


Ember.Table.RowArrayProxy.reopen({
  rowContent: function() {
    return []; 
  }.property('content.@each')
});