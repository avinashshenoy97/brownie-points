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
      resetForm();
    },
   submitCoins: function() {
      Vue.http.put('/wallet/wallet/sendCoins',this.sendCoins)
          .then((response) => {
            console.log("sent",response);
            this.transactionNumber=response.data['transactionNumber']
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
      transactionDetails:{},
      transactionDetailsAddr:[],
      transactionDetailsCoins:[]
    }
  },
  methods:{
    cancel3: function(){
      this.$parent.formOpen3 = false;
      this.$parent.formClose3 = true;
    },
    getTransactionDetails: function() {
      this.$http.get('/wallet/wallet/getTransactionDetails',this.transactionDetails)
          .then((response) => {
            console.log("received",response.data);
            this.transactionDetailsAddr=response.data['transactionAddr'];
            this.transactionDetailsCoins=response.data['transactionCoins'];
            this.updateTransactions();
            console.log("gotit",this.transactionDetailsAddr);
          })
          .catch((err) => {
            console.log(err);
          })
     },
     updateTransactions: function(){
        var $transactionDetailsAddr = this.transactionDetailsAddr;
        var $transactionDetailsCoins = this.transactionDetailsCoins;
        var i=1;
        if($transactionDetailsAddr.length>0)
          $(".container-right").empty();
        for(i=0;i<$transactionDetailsAddr.length;i++){ 
          var j=i+1;
          // var $addr=$transactionDetails[i].txOuts[0].address;
          // var $coinCount = $transactionDetails[i].txOuts[0].coinCount;
          var $addr=$transactionDetailsAddr[i];
          var $coinCount=$transactionDetailsCoins[i];
          var $myaddr = vue.$refs.public_address.publicaddress
          var $transaction = "<div class='container'>";
          $transaction+= "<div class='card'>"
          $transaction+= "<div class='front'><h2>Transaction "+j+"</h2></div>"
          $transaction+= "<div class='back'>"
          $transaction+= "<div class='content'>"
          $transaction+= "<h3 class='cardTitle'>Sender Address</h3>"
          $transaction+= "<p class='cardContent' title='"+$myaddr+"'>"+$myaddr+"</p>"
          $transaction+= "<h3 class='cardTitle'>Receiver Address</h3>"
          $transaction+= "<p class='cardContent'>"+$addr+"</p>"
          $transaction+= "<h3 class='cardTitle'>Number of Coins</h3>"
          $transaction+= "<p class='cardContent'>"+$coinCount+"</p>"
          // $transaction+= "<h3 class='cardTitle'>Timestamp</h3>"
          // $transaction+= "<p class='cardContent'>1234</p>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          var $transaction_el = $($transaction);
          $(".container-right").append($transaction_el);
        }
        $('.card').unbind('click');
        $('.card').click(function(){
          $(this).toggleClass('flipped');
        });

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
  },
  mounted(){
    this.getPublicAddress();
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
      vue.$refs.transaction_status.getTransactionDetails();
      this.formOpen3 = arg1;
    },
    cancel1: function(){
      this.formOpen1 = false;
      this.formClose1 = true;
      resetForm();
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