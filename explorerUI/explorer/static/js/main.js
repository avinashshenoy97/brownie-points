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
    },
    setStateValue: function(){
      this.stateOpen = true;
      $('#closeButton').css("opacity","0");
      $('.btn-paginacao').css("z-index","-1");
    },
   getBlocks: function() {
      Vue.http.get('/explorer/getBlocks',{})
          .then((response) => {
            console.log("sent",response);
            // this.transactionNumber=response.data['transactionNumber']
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
    },
  getPoolData:function(){
      Vue.http.get('/explorer/getPoolData',{})
          .then((response) => {
            
          })
          .catch((err) => {
            console.log("error",err);
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
        $(this).find('.senderAddr:not(:contains("'+txt+'"))').parent().parent().parent().parent().hide();      
        $(this).find('.recAddr:contains("'+txt+'")').parent().parent().parent().parent().show();      
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