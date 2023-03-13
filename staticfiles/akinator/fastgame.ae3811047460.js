var question = document.querySelector("#questionid");
var yes = document.querySelector("#yes");
var idk = document.querySelector("#idk");
var no = document.querySelector("#no");
var pkdata = document.querySelector("#pkdata");
var flagdata = document.querySelector("#flagdata");
var histdata = document.querySelector("#histdata");
var submitname = document.querySelector("#submitname");

class Member{
	constructor(times_searched, pk){
		this.times_searched=times_searched;
		this.pk=pk;
	}
}
class Question{
	constructor(question_text, pk){
		this.question_text=question_text;
		this.pk=pk;
	}
}
class Data{
	constructor(times_yes, times_total, member, question){
		this.times_yes=times_yes;
		this.times_total=times_total;
		this.member=member;
		this.question=question;
	}
}
membersL=[]
questionsL=[]
datasL=[]
//
for(var i=0;i<mp.length;i++){
    newmem = new Member(Number(mts[i]), Number(mp[i]));
    membersL.push(newmem);
}
for(var i=0;i<Number(qp.length);i++){
    newques = new Question(qqt[i], Number(qp[i]));
    questionsL.push(newques);
}
for(var i=0;i<Number(dp.length);i++){
    newdat = new Data(Number(dty[i]), Number(dtt[i]), dmp[i], dqp[i]);
    datasL.push(newdat);
}
//
members={}
questions={} // questions[pk]=question object and similarly for others
datas={}
for(var i in membersL){
	members[membersL[i].pk]=membersL[i];
}
for(var i in questionsL){
	questions[questionsL[i].pk]=questionsL[i];
}
for(var i in membersL){
	datas[Number(membersL[i].pk)]={};
}
for(var i in datasL){
	datas[Number(datasL[i].member)][Number(datasL[i].question)]=datasL[i];
}
//---------------------------------------------------------------------------------------
// this is equivalent to 'prob_list' of the user
total_searches=Number(0);
prob_list={};
history='';
// this is equivalent to 'history' of the user
questions_asked=[];
answers_given=[];
for(var mpk in members){
	total_searches+=Number(members[mpk].times_searched);
}
for(var mpk in members){
	prob_list[Number(mpk)]=Number(Number(members[mpk].times_searched)/Number(total_searches));
}
// these are the questions left for the algo to ask
questions_left = new Set();
for(var qpk in questions){
	questions_left.add(Number(qpk));
}
function max(a){
	var q = -1;
	for(var i in a){
		q=Math.max(Number(q),Number(a[i]));
	}
	return(q);
}
function min(a){
	var q = 2;
	for(var i in a){
		q=Math.min(Number(q),Number(a[i]));
	}
	return(q);
}
function fadeIn(object){
	var t=70;
	var op = 0;
	var i=0;
	function update(){ 
		if((i===t)||(op>0.99)){
			;
		}else{
			op+=(1/t);
			object.style.opacity=op;
			setTimeout(update,1);
			i++;
		}
	}
	update();
}
function animate(){
    fadeIn(yes);
    fadeIn(idk);
    fadeIn(no);
}
function get_best_question(){
	score={};
	for(var qpk of questions_left){
		var pogo = 0; // prob of getting one
		for(var mpk in prob_list){
			pogo += (Number(prob_list[mpk]))*(Number(datas[mpk][qpk].times_yes)/Number(datas[mpk][qpk].times_total)); 
		}
		score[qpk]=Math.abs((0.5)-Number(pogo));
	}
	var min_score = Number(min(score));
	for(var qpk in score){
		if((Number(score[qpk])-Number(min_score))<Number(1e-4)){
			return(qpk);
		}
	}
	return(-1);
}

function refresh(answer){
	if((Number(questions_asked.length))!==0){
		// the 'POST' part begins here
		// ----------------
		// updating history
		answers_given.push(Number(answer));
		// Updating the prob_list data based on main algo
	    // Note that if the answer is -1 (when the user doesn't know) prob list does not change
	    var qpk=Number(questions_asked[questions_asked.length-1]);
		if(answer!==0){
			var tot=0;
			for(var mpk in prob_list){
				var thedat = datas[Number(mpk)][Number(qpk)];
				var pyes = Number(thedat.times_yes)/Number(thedat.times_total);
				if(Number(answer)===1) prob_list[mpk]*=Number(pyes);
				else prob_list[mpk]*=Number(1-Number(pyes));

				tot+=Number(prob_list[mpk]);
			}
			for(var mpk in prob_list){
				prob_list[mpk]/=Number(tot);
			}
		}
	}
	// the 'GET' part begins here
	// ----------------------------
	var new_question_pk=Number(get_best_question());
	// checking if it is time to end this
	var flag2=[false];
	for(var mpk in prob_list){
		if(prob_list[Number(mpk)]>0.5){
			flag2[0]=true;
			flag2.push(mpk);
		}
	}
	// checking if max limit of questions has exceeded
	var flag3=(Number(questions_asked.length)>=12);
	// checking if further narrowing down is not possible with the available questions
	var flag4=false;
	if(Number(questions_asked)!==0){
        flag4 = (new_question_pk in questions_asked);
	}
	// checking against don't know button exploitation for multiple answers
	var flag5=Number(max(prob_list))>Number(0.21);

	if(flag2[0]||flag3||flag4){
		// serve the result page
		// send the appropriate data back to the database
        
		var maxProb = max(prob_list);
        var maxProb_mpks = [];
		for(var mpk in prob_list){
			if(Number(maxProb)-Number(prob_list[mpk])<Number(5e-3)){
				maxProb_mpks.push(Number(mpk));
			}
		}
        var result_pks = [];
        var flags=[];
        
        if(flag2[0]){
            result_pks.push(flag2[1]);
        }else if(flag3||flag4){
            if(flag5){
                result_pks = [...maxProb_mpks];
            }else{
                result_pks = [maxProb_mpks[0]];
            }
        }else{
            console.log('TNP');
            console.assert(false);
        }
        result_pks=result_pks.join('.');
        pkdata.value=result_pks;
        
        if(flag2[0]) flags.push(2);
        if(flag5) flags.push(5);
        flags=flags.join('.');
        flagdata.value=flags;
        
		var history=[];
		for(var i=0;i<questions_asked.length;i++){
			if(Number(answers_given[i])===1) history.push(questions_asked[i]+',1');
			else if(Number(answers_given[i])===-1) history.push(questions_asked[i]+',0');
			else if(Number(answers_given[i])===0) history.push(questions_asked[i]+',-1');
			else console.log('TNP');
		}
		history=history.join('/');        
        histdata.value=history;
        
        submitname.submit();
	}
	questions_asked.push(Number(new_question_pk));
	questions_left.delete(new_question_pk);
    // an API request here (in future)., to get the question form server using only its pk
	question.textContent=questions[new_question_pk].question_text;
    animate();
}


function refresh_1(){
	var answer = 1;
	refresh(answer);
}
function refresh_0(){
	var answer=0;
	refresh(answer);
}
function refresh_m1(){
	var answer=-1;
	refresh(answer);
}

yes.addEventListener("click",refresh_1);
idk.addEventListener("click",refresh_0);
no.addEventListener("click",refresh_m1);
refresh(1);