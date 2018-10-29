createBlock = function(){
	count=5;
	var $blockDiv = "<div class='vitrine"+count+"' vitrine'><div class='line line"+count+"'>-</div><h2>Pagina "+count+"</h2><li>Vitrine</li><li>Vitrine</li><li>Vitrine</li><li>Vitrine</li></div>";
	var $blockDiv_el = $($blockDiv);
	$('#blocks').append($blockDiv_el);
	line1=Math.round(parseFloat($('.line1').css("top"))/($(window).height()-20) * 100);
	line1=line1-4;
	for(var i=2;i<count;i++){
		var linename = ".line"+i;
		line1=line1+(100/count);
		$(linename).css("top",line1.toString()+"%");
		
	}
	console.log(line1);

	$(".line"+count).css("top",(line1+(100/count)).toString()+"%");
	$(".line"+count).css("width","80%");

	$('#paginacao5:checked ~ .box-vitrines > ul').css({"transition":"transform .7s ease-in-out","transform":"translateY(-80%)"});
	$('#paginacao5:checked ~ .box-vitrines label[for="paginacao5"]').css({"background-color":"#FF1493","color":"#FFF"});

console.log(document.querySelector('#paginacao2'), ':checked');
for(var i=2;i<count;i++){
	
	blockName = "#paginacao"+i+":checked ~ .box-vitrines > ul";
	$(blockName).css({"transition":"transform .7s ease-in-out","transform":"translateY(-80%)"}) = 
}

window.getComputedStyle(
	document.querySelector('.element'), ':before'
).getPropertyValue('color')
}