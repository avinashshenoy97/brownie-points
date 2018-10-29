var menuVue = new Vue({
  el: '#menu-container',
  data: {
    menuOpen1: false,
    menuOpen2: false,
    menuOpen3: false,
    menuOpen4: false,
    menuOpen5: false
  },
  methods: {
    cancelMenu: function(){
          this.menuOpen1= false,
          this.menuOpen2= false,
          this.menuOpen3= false,
          this.menuOpen4= false,
          this.menuOpen5= false
    }
  }
});