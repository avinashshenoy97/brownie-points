var sendCoinsComp=Vue.component('send-coins-comp',{
    data: function(){
    return{
    sendCoins:{
        address:null,
        coinCount:0,
      },
    transactionNumber:0
    }
  },
  methods:{
    cancel1: function(){
      this.$parent.formOpen1 = false;
      this.$parent.formClose1 = true;
    },
   submitCoins: function() {
      Vue.http.put('/wallet/wallet/sendCoins',this.sendCoins)
          .then((response) => {
            console.log("sent",response);
          })
          .catch((err) => {
            console.log("error",err);
          })
     }
  }
});

var transactionStatus=Vue.component('transaction-status',{
  data:function(){
    return{
      transactionDetails:{

      }
    }
  },
  methods:{
    cancel3: function(){
      this.$parent.formOpen3 = false;
      this.$parent.formClose3 = true;
    },
    getTransactionDetails: function() {
      this.$http.get('/getTransactionDetails',this.transactionDetails)
          .then((response) => {
            console.log("received",response);
          })
          .catch((err) => {
            console.log(err);
          })
     } 
  }
});

var balance=Vue.component('balance',{
  data:function(){
    return{
      balanceCoins:0
    }
  },
  methods:{
    cancel2: function(){
      this.$parent.formOpen2 = false;
      this.$parent.formClose2 = true;
    },
    getBalance: function() {
      this.$http.get('/wallet/wallet/getBalance',this.transactionDetails)
          .then((response) => {
            console.log("received",response.data);
            this.balanceCoins=response.data['balance']
          })
          .catch((err) => {
            console.log(err);
          })
     } 
  }
});

var publicAddress=Vue.component('public-address',{
  data:function(){
    return{
      publicaddress:null
    }
  },
  methods:{
    getPublicAddress: function() {
      this.$http.get('/wallet/wallet/getPublicAddress',this.publicaddress)
          .then((response) => {
            console.log("received",response.data);
            this.publicaddress=response.data['publicKey']
          })
          .catch((err) => {
            console.log(err);
          })
     }      
  }
});

var vue = new Vue({
  el: '#app',
  delimiters:["[[","]]"],
  data: function(){
    return{
    formOpen1: false,
    formClose1:false,
    formOpen2: false,
    formClose2:false,
    formOpen3: false}
  },
  components:{
    'send-coins-comp':sendCoinsComp,
    'transaction-status':transactionStatus,
    'public-address': publicAddress
  },
  methods: {
    setValue1: function(arg1,arg2){
      this.formOpen1 = arg1;
      this.formClose1 = arg2;
      // console.log(this.step,this.progressValue)
    },
    setValue2: function(arg1,arg2){
      this.formOpen2 = arg1;
      this.formClose2 = arg2;
      vue.$refs.get_balance.getBalance();
    },
    setValue3: function(arg1){
      this.formOpen3 = arg1;
    },
    cancel1: function(){
      this.formOpen1 = false;
      this.formClose1 = true;
      this.sendCoins = {
        address:null,
        coinCount:0
      }
    },
    cancel2: function() {
      this.formOpen2 = false;
      this.formClose2 = true;
      // setTimeout(() => this.formClose2 = false, 1000);      
    },
    cancel3: function(){
      this.formOpen3 = false;
    }
  }
});

    window.onclick = function(event) {
    var forminner = document.getElementById("homeModal");
    var sendCoinsOuter = document.getElementById("sendCoinsOuter");
    if(sendCoinsOuter.classList.contains('open')){    
    if (event.target == sendCoinsOuter) {
        vue.$refs.send_coins.cancel1();
        }
      }
    };