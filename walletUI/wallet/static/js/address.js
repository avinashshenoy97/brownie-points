var acc = document.getElementById("accordion");
var i;
addr=''

// for (i = 0; i < acc.length; i++) {
  var address = function(event) {
    // this.classList.toggle("active");
    var panel = event.target.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      // panel.style.maxHeight = panel.scrollHeight + "px";
      panel.style.maxHeight = "30vh";
      if(addr=='' || addr==null){
        vue.$refs.public_address.getPublicAddress();
        addr=vue.$refs.public_address.publicaddress
      }
      panel.innerHTML = addr;
    } 
  };
// }
