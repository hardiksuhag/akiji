var everything = document.querySelector("body");

function fadeIn(){
	op = Number(everything.style.opacity)
	if(op<0.999){
		everything.style.opacity = String(op + Number(1/100))
		setTimeout(fadeIn,1);
	}else{
		everything.style.opacity="1";
		return;
	}
}
everything.style.opacity="0";
fadeIn();
