
var vueApp = new Vue({
  el: '#app',
  data: () => ({
    dialog: false,
    items: [
      { title: 'Dashboard', icon: 'dashboard' },
      { title: 'Account', icon: 'account_box' },
      { title: 'Admin', icon: 'gavel' },
    ],
   
  }),


  
  methods: {
    initialize() {
     
    },

  }
})