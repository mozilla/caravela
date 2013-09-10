App.InfoHotspotComponent = Em.Component.extend({
  tagName: "i",
  classNames: ["icon-info-sign"],



  didInsertElement: function(){
    console.log()

    var pop = this.$().popover({
      placement: 'left',
      title: this.get('title'),
      html: true,
      content: this.get('body'),
      container: this.$().parent(),
    });
    
  }


})