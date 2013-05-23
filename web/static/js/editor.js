App.reopen({
  EditorView: Em.View.extend({
    classNames: ["Editor"],
    
    content: "",
    willDestroyElement: function(){
      console.log('destroying view');
      this.editor = null;
    },
    didInsertElement: function(){
      // map command-save from anywhere to save(), it would be
      // nice if this was an event at the app level
      
      var content = this.get("content") || '';
      var element = this.get("element");
      this.editor = CodeMirror(
        function(elt){
          element.appendChild(elt, element);
        },
        {
          mode: {name: "javascript", json: true},
          value: content
        }
      );
      var self = this;
      
      this.editor.on("change", function(){
        self.set("content", self.editor.getValue());
      });
      
    },
    
    contentDidChange:function(){
      var content = this.get("content");

      if(this.editor.getValue() != content){
        this.editor.setValue(content);
      }
      
      return content;
    }.observes("content"), 
  })

})
