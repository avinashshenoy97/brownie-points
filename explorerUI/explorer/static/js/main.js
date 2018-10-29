var blockState=Vue.component('block-state-comp',{
    data: function(){
    return{
    sendCoins:{
        address:null,
        coinCount:0,
      },
    checkbalance:0,
    stateOpen:false
    }
  },
  methods:{
    cancelState: function(){
      this.stateOpen=false;
      $('.btn-paginacao').css("z-index","0");
      $('#closeButton').css("opacity","1");
      console.log("here1");
    },
    setStateValue: function(){
      this.stateOpen = true;
      $('.btn-paginacao').css("z-index","-1");
      $('#closeButton').css("opacity","0");

    },
   submitCoins: function() {
      Vue.http.put('/wallet/sendCoins',this.sendCoins)
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

var transactionPool=Vue.component('transaction-pool',{
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
    }
    // getTransactionDetails: function() {
    //   this.$http.get('/wallet/getTransactionDetails',this.transactionDetails)
    //       .then((response) => {
    //         console.log("received",response.data);
    //         this.transactionDetailsAddr=response.data['transactionAddr'];
    //         this.transactionDetailsCoins=response.data['transactionCoins'];
    //         this.updateTransactions();
    //         console.log("gotit",this.transactionDetailsAddr);
    //       })
    //       .catch((err) => {
    //         console.log(err);
    //       })
    //  },
    //  updateTransactions: function(){
    //     var $transactionDetailsAddr = this.transactionDetailsAddr;
    //     var $transactionDetailsCoins = this.transactionDetailsCoins;
    //     var i=1;
    //     if($transactionDetailsAddr.length>0)
    //       $(".container-right").empty();
    //     for(i=0;i<$transactionDetailsAddr.length;i++){ 
    //       var j=i+1;
    //       // var $addr=$transactionDetails[i].txOuts[0].address;
    //       // var $coinCount = $transactionDetails[i].txOuts[0].coinCount;
    //       var $addr=$transactionDetailsAddr[i];
    //       var $coinCount=$transactionDetailsCoins[i];
    //       var $myaddr = vue.$refs.public_address.publicaddress
    //       var $transaction = "<div class='container'>";
    //       $transaction+= "<div class='card'>"
    //       $transaction+= "<div class='front'><h2>Transaction "+j+"</h2></div>"
    //       $transaction+= "<div class='back'>"
    //       $transaction+= "<div class='content'>"
    //       $transaction+= "<h3 class='cardTitle'>Sender Address</h3>"
    //       $transaction+= "<p class='cardContent' title='"+$myaddr+"'>"+$myaddr+"</p>"
    //       $transaction+= "<h3 class='cardTitle'>Receiver Address</h3>"
    //       $transaction+= "<p class='cardContent'>"+$addr+"</p>"
    //       $transaction+= "<h3 class='cardTitle'>Number of Coins</h3>"
    //       $transaction+= "<p class='cardContent'>"+$coinCount+"</p>"
    //       // $transaction+= "<h3 class='cardTitle'>Timestamp</h3>"
    //       // $transaction+= "<p class='cardContent'>1234</p>"
    //       $transaction+= "</div>"
    //       $transaction+= "</div>"
    //       $transaction+= "</div>"
    //       $transaction+= "</div>"
    //       var $transaction_el = $($transaction);
    //       $(".container-right").append($transaction_el);
    //     }
    //     $('.card').unbind('click');
    //     $('.card').click(function(){
    //       $(this).toggleClass('flipped');
    //     });

    //  } 
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
    'block-state-comp':blockState,
    'transaction-pool':transactionPool,
  },
  methods: {
    setValue1: function(arg1,arg2){
      this.formOpen1 = arg1;
      this.formClose1 = arg2;
      // createBlock();
      // console.log(this.step,this.progressValue)
    },
    setValue2: function(arg1,arg2){
      this.formOpen2 = arg1;
      this.formClose2 = arg2;
      vue.$refs.get_balance.getBalance();
    },
    setValue3: function(arg1){
      // vue.$refs.transaction_status.getTransactionDetails();
      $('.card').click(function(){
          console.log("here");
          $(this).toggleClass('flipped');
        });

      $('#blockVal').change(function(){
        var $container = $(".container-cards> .container");
        if( ($(this).val()=='' || $(this).val()=='the_default_value') && $(this).attr('type')!='hidden') { 
          $container.show();
        }
        else{
        $container.each(function(){
        var txt = $('#blockVal').val();
        $(this).find('#txnNo:not(:contains("'+txt+'"))').parent().parent().parent().hide();      
      });
      }
    });

      $('#blockAddr').change(function(){
        var $container = $(".container-cards> .container");
        if( ($(this).val()=='' || $(this).val()=='the_default_value') && $(this).attr('type')!='hidden') { 
          $container.show();
        }
        else{
        $container.each(function(){
        var txt = $('#blockAddr').val();
        $(this).find('.cardContent:not(:contains("'+txt+'"))').parent().parent().parent().parent().hide();      
      });
      }
    });

      this.formOpen3 = arg1;
    },
    cancel1: function(){
      this.formOpen1 = false;
      this.formClose1 = true;
      $('.btn-paginacao').css("z-index","0");
      $('#closeButton').css("opacity","1");
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

    // window.onclick = function(event) {
    // var forminner = document.getElementById("homeModal");
    // var sendCoinsOuter = document.getElementById("blockStateOuter");
    // if(sendCoinsOuter.classList.contains('open')){    
    // if (event.target == sendCoinsOuter) {
    //     vue.$refs.block_state.cancel1();
    //     }
    //   }
    // };