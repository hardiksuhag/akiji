function get_proper_name(name){
	var names = name.split('.');
	for(var i=0;i<names.length;i++){
		names[i]
		names[i]=names[i][0].toUpperCase()+names[i].slice(1,names[i].length).toLowerCase();
	}
	return(names.join(' '));
}

for(var i=0;i<4;i++){
	curr_button = document.querySelector("#b"+String(i));
    if(i<chosen_names.length){
    	curr_button.hidden=false;
    	curr_button.value=chosen_names[i];
    	curr_button.textContent=get_proper_name(chosen_names[i]);
    }else{
    	curr_button.hidden=true;
    }
}
