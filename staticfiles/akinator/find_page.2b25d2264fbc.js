var search_bar = document.querySelector("#search_bar");
var size_of_search = 0

// var all_names=name_dat.split('!');
// all_names has already been generated in the html file script tag

function get_proper_name(name){
	var names = name.split('.');
	for(var i=0;i<names.length;i++){
		names[i]=names[i][0].toUpperCase()+names[i].slice(1,names[i].length).toLowerCase();
	}
	return(names.join(' '));
}

function changeNames(){
	if(Number(search_bar.value.length)===0){
		size_of_search=0;
		for(var i=0;i<5;i++){
			var result = document.querySelector("#r"+String(i+1));
			result.hidden=true;
		}
	}
	if(size_of_search!==Number(search_bar.value.length)){
		top_names = search(all_names,search_bar.value,5);
		size_of_search = Number(search_bar.value.length);
		for(var i=0;i<5;i++){
			result_id_query=("#r"+String(i+1));
			var result = document.querySelector(result_id_query);
			result.textContent = get_proper_name(top_names[i]);
			result.value = top_names[i];
			result.hidden=false;
		}
	}
}

function search (name_list, name_searched, count) {
	function dist(a,b,i){
		var p1=Number(i);
		var p2=Number(i);
		var b1=false;
		var b2=false;
		while((0<=p1)&&(p1<b.length)){
			if(a[i]===b[p1]) break;
			p1--;
		}
		while((0<=p2)&&(p2<b.length)){
			if(a[i]===b[p2]) break;
			p2++;
		}
		b1=((0<=p1)&&(p1<b.length));
		b2=((0<=p2)&&(p2<b.length));
		if(b1&&b2) return(Math.min(Math.abs(p1-i),Math.abs(p2-i)));
		else if(b1&&(!b2)) return(Math.abs(p1-i));
		else if((!b1)&&b2) return(Math.abs(p2-i));
		else return(-1);
	}
	function f(x){
		var smth = (Math.exp(1))**(x);
		return((smth)/((1+smth)**2));
	}
	function score(test_name_taken){
		var test_names_all=test_name_taken.split('.');
		var scr_final=0;
		test_names_all.forEach(function(test_name){
			var a=[]
			var b=[]
			a.push(...(name_searched.toLowerCase()));
			b.push(...(test_name.toLowerCase()));
			var scr=0;
			for(var i=0;i<a.length;i++){
				d=dist(a,b,i);
				if(d===-1) continue;
				else scr+=f(d);
			}
			scr/=a.length;
			scr_final=Math.max(scr_final,scr);
		});
		return(scr_final);
	}
	function comp(name1,name2){
		if(score(name1)==score(name2)) return(0);
		if(score(name1)<score(name2)) return(-1);
		return(1);
	}
	name_list.sort(comp);
	name_list.reverse();
	return(name_list.slice(0,count));
}

search_bar.addEventListener("keyup",changeNames);
changeNames();