var acc = document.getElementById("accordion");
var i;

  var address = function(event) {
    var panel = event.target.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = "30vh";
      addr=vue.$refs.public_address.publicaddress
      panel.innerHTML = addr;
    } 
  };
// }
