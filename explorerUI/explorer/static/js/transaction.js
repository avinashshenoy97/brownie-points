var sortAcc = function(event) {
    var panel = event.target.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = "30vh";
    } 
  };

var searchAcc = function(event) {
    var panel = event.target.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
      panel.style.paddingTop = "0";
      panel.style.paddingBottom = "0";
    } else {
      panel.style.maxHeight = "30vh";
      panel.style.paddingTop = "10%";
      panel.style.paddingBottom = "8%";
    } 
  };

 var filterAcc = function(event) {
    var panel = event.target.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
      panel.style.paddingTop = "0";
      panel.style.paddingBottom = "0";
    } else {
      panel.style.maxHeight = "30vh";
      panel.style.paddingTop = "10%";
      panel.style.paddingBottom = "8%";
    } 
  };

  var sortOld = function(event){
  	var $container = $(".container-cards> .container");
  	var sortedOld=$container.sort(function (a, b) {
        return $(a).find("#txnNo").text()>$(b).find("#txnNo").text();
    });
    $(".container-cards").html(sortedOld);
  }


    var sortNew = function(event){
  	var $container = $(".container-cards> .container");
    var sortedNew=$container.sort(function (a, b) {
        return $(a).find("#txnNo").text()<$(b).find("#txnNo").text();
    });
    $(".container-cards").html(sortedNew);
  }
