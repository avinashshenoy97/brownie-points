var blockState=Vue.component('block-state-comp',{
    data: function(){
    return{
      completedTxAddr:[],
      completedTxSenderAddr:[],
      completedTxAmt:[],
      stateOpen:false
    }
  },
  methods:{
    cancelState: function(){
      // this.stateOpen=false;
    },
    setStateValue: function(){
      this.stateOpen = true;

    },
   getBlocks: function() {
      Vue.http.get('/explorer/getBlocks',{})
          .then((response) => {
            console.log("sent",response);
            // this.transactionNumber=response.data['transactionNumber']
            this.completedTxAddr=response.data['completedTxAddr'];
            this.completedTxSenderAddr=response.data['completedTxSenderAddr'];
            this.completedTxAmt=response.data['completedTxAmt'];
            this.updateBlocks();
          })
          .catch((err) => {
            console.log("error",err);
          })
     },
    updateBlocks: function(){
      $completedTxAddr = this.completedTxAddr;
      $completedTxSenderAddr = this.completedTxSenderAddr;
      $completedTxAmt = this.completedTxAmt;
      console.log($completedTxAddr);
      for(i=0;i<$completedTxAddr.length;i++){
        j=i+1;
        $blockParentNo=Math.ceil(j/4)-1;
        $blockNo = j%4 + 1;
        $blockDataNo = $blockNo + 4;
        $blockData="<div class='stateModal' >";
        $blockData+="<div id='closeStateButton'><span>&times</span></div>";
        $blockData+="<div id='blockModal'>";
        $blockData+="<span id='blockContent'><h3>Sender Address : </h3><span>"+$completedTxSenderAddr[i]+"</span></span>";
        $blockData+="<span id='blockContent'><h3>Receiver Address : </h3><span>"+$completedTxAddr[i]+"</span></span>";        
        $blockData+="<span id='blockContent'><h3>Number Of Coins : </h3><span>"+$completedTxAmt[i]+"</span></span></div></div>";
        
        $blockData_el=$($blockData);
        $('#blocks').children().eq($blockParentNo).append($blockData_el);
        $('#blocks').children().eq($blockParentNo).children().eq($blockNo).css('background-color','#71bc78');
        
        $('#closeStateButton').click(function(){
          console.log($(this));
          $(this).parent().removeClass('open');
          $('.btn-paginacao').css("z-index","0");
          $('#closeButton').css("opacity","1");

        });

        $('#blocks').children().eq($blockParentNo).children().eq($blockNo).click(function(){
          $('#blocks').children().eq($blockParentNo).children().eq($blockDataNo).addClass('open');
          $('#closeButton').css("opacity","0");
          $('.btn-paginacao').css("z-index","-1");
        });
      }
    }
  }
});

var transactionPool=Vue.component('transaction-pool',{
  data:function(){
    return{
      transactionDetails:{},
      transactionDetailsAddr:[],
      transactionDetailsAddrSender:[],
      transactionDetailsCoins:[]
    }
  },
  methods:{
    cancel3: function(){
      this.$parent.formOpen3 = false;
      this.$parent.formClose3 = true;
    },
  getPoolData:function(){
      this.$http.get('/explorer/getPoolData',{})
          .then((response) => {
          this.transactionDetailsAddr=response.data['transactionAddr'];
          this.transactionDetailsAddrSender=response.data['transactionAddrSender'];
          this.transactionDetailsCoins=response.data['transactionCoins'];
          this.updateTransactionPool();
          })
          .catch((err) => {
            console.log("error",err);
          })
    },
    updateTransactionPool:function(){
        var $transactionDetailsAddr = this.transactionDetailsAddr;
        var $transactionDetailsAddrSender = this.transactionDetailsAddrSender;    
        var $transactionDetailsCoins = this.transactionDetailsCoins;
        var i=1;
        if($transactionDetailsAddr.length>0)
          $(".container-cards").empty();
        for(i=0;i<$transactionDetailsAddr.length;i++){ 
          var j=i+1;
          // var $addr=$transactionDetails[i].txOuts[0].address;
          // var $coinCount = $transactionDetails[i].txOuts[0].coinCount;
          var $addr=$transactionDetailsAddr[i];
          var $coinCount=$transactionDetailsCoins[i];
          var $myaddr = $transactionDetailsAddrSender[i];
          var $transaction = "<div class='container'>";
          $transaction+= "<div class='card'>"
          $transaction+= "<div class='front'><h2 id='txnNo'>Transaction "+j+"</h2></div>"
          $transaction+= "<div class='back'>"
          $transaction+= "<div class='content'>"
          $transaction+= "<h3 class='cardTitle'>Sender Address</h3>"
          $transaction+= "<p class='cardContent senderAddr' title='"+$myaddr+"'>"+$myaddr+"</p>"
          $transaction+= "<h3 class='cardTitle'>Receiver Address</h3>"
          $transaction+= "<p class='cardContent recAddr'>"+$addr+"</p>"
          $transaction+= "<h3 class='cardTitle'>Number of Coins</h3>"
          $transaction+= "<p class='cardContent'>"+$coinCount+"</p>"
          // $transaction+= "<h3 class='cardTitle'>Timestamp</h3>"
          // $transaction+= "<p class='cardContent'>1234</p>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          $transaction+= "</div>"
          var $transaction_el = $($transaction);
          $(".container-cards").append($transaction_el);
        }

        $('.card').unbind('click');
        $('.card').click(function(){
          $(this).toggleClass('flipped');
        });

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
      vue.$refs.block_state.getBlocks();
    },
    // setValue2: function(arg1,arg2){
    //   this.formOpen2 = arg1;
    //   this.formClose2 = arg2;
    // },
    setValue3: function(arg1){
      vue.$refs.transaction_pool.getPoolData();
      $('.card').click(function(){
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
        console.log(txt);
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
