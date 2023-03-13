from django.shortcuts import render
from django.http import HttpResponse
from .models import Name, User, Member, Question, Data, Search
from .search_algo import search
from datetime import datetime
from . import akinator_algo
from . import gigs
import json

# Utility functions
def seconds():
    tm = list(map(int, datetime.now().time().strftime("%H:%M:%S").split(':')))
    return((tm[0]*3600)+(tm[1]*60)+(tm[2]*1))

def prob_list_new():
    pln = ''
    tot_srch = 0
    for member in Member.objects.all():
        tot_srch += int(member.times_searched)
    for member in Member.objects.all():
        pln += str(member.pk)
        pln += ','
        pln += str((int(member.times_searched))/tot_srch)
        pln += '/'
    return(pln.strip('/'))


def prob_list_updated(prob_context, question_pk, answer):
    prob_old = dict(prob_context)
    for someProb in Data.objects.all():
        if((someProb.question.pk==question_pk) and (someProb.member.pk in prob_old)):
            pyes = int(someProb.times_yes)/int(someProb.times_total)
            pno = 1-pyes
            if(answer): prob_old[someProb.member.pk] *= pyes
            else: prob_old[someProb.member.pk] *= pno
    sum_prob = 0
    for someMemberPk in prob_old:
        sum_prob += prob_old[someMemberPk]
    # generating the string
    q = []
    for someMemberPk in prob_old:
        q.append(str(someMemberPk)+','+str(prob_old[someMemberPk]/sum_prob))
    return('/'.join(q))

def best_question_pk(prob_context, remaining_questions):
    prob_yes_dat = {}  # for e.g. prob_yes_dat[member_pk][question_pk]
    for someMemberPk in prob_context:
        prob_yes_dat[someMemberPk] = {}
    for someProb in Data.objects.all():
        if((someProb.member.pk in prob_yes_dat) and (someProb.question.pk in remaining_questions)):
            prob_yes_dat[someProb.member.pk][someProb.question.pk] = int(someProb.times_yes)/int(someProb.times_total);
    return(akinator_algo.get_best_question_pk(prob_context, prob_yes_dat, remaining_questions))

def get_message(ansMembersNames):
    if(len(ansMembersNames)>1):
        assert(0)
    else:
        ans = '.'.join(ansMembersNames[0].split(' '))
        return(gigs.get_msg(ans))

# function for updating the database 
def update(selected_name, history, ip_address_of_user, corr_stat):
    new_search = Search(name_searched=selected_name, search_time=datetime.now(), ip_address=ip_address_of_user, is_correct=corr_stat)
    new_search.save()
    # if blank string given as answer, no data is submitted
    print('name: ', selected_name)
    print('history: ', history)
    print('time_active: ', datetime.now())
    if(selected_name.strip(' ')==''):
        return
    for a_name in Name.objects.all():
        if(a_name.name_text==selected_name):
            name_pk = a_name.pk
            currName = Name.objects.get(pk=name_pk)
            currName.search_count = str(int(currName.search_count)+1)
            currName.save()
            break
    #
    flag = False
    member_pk = 0
    # checking if the person already exists in the database or not
    for a_mem in Member.objects.all():
        if(a_mem.member_name==selected_name):
            flag = True
            member_pk = a_mem.pk
            break
    # what to do if the person already exists in the database
    if(flag):
        currMem = Member.objects.get(pk=member_pk)
        currMem.times_searched = str(int(currMem.times_searched)+1)
        currMem.save()
        hist_list = (history.strip('/')).split('/')
        hist_dict = {}
        for hist_item in hist_list:
            hist_dict[int((hist_item.split(','))[0])]=int((hist_item.split(','))[1])
        for a_dat in Data.objects.all():
            if((a_dat.question.pk in hist_dict) and (a_dat.member.pk==member_pk)):
                # obtain the answer given
                ans_gvn = hist_dict[a_dat.question.pk]
                # if answer was "don't know" no action is taken and the loop is continued
                if(ans_gvn==-1):
                    continue
                # now increase times_total by 2
                a_dat.times_total = str(int(a_dat.times_total)+2)
                a_dat.save()
                # if no, increase times_yes by 0
                if(ans_gvn==0):
                    continue
                # if yes, increase times_yes by 2
                elif(ans_gvn==1):
                    a_dat.times_yes = str(int(a_dat.times_yes)+2)
                    a_dat.save()
                # in all other cases raise error
                else:
                    assert(0)
    # what to do if the person doesn't exist in the database
    else:
        new_mem = Member(member_name=selected_name, times_searched="2")
        new_mem.save()
        member_pk = new_mem.pk
        currMem = Member.objects.get(pk=member_pk)
        hist_list = (history.strip('/')).split('/')
        hist_dict = {}
        for hist_item in hist_list:
            hist_dict[int((hist_item.split(','))[0])]=int((hist_item.split(','))[1])
        for a_ques in Question.objects.all():
            question_pk = a_ques.pk
            new_dat = Data(question=Question.objects.get(pk=question_pk), member=Member.objects.get(pk=member_pk))
            new_dat.save()
            if(question_pk in hist_dict):
                ans_gvn = hist_dict[question_pk]
                if(ans_gvn==-1):
                    new_dat.times_yes = 2
                    new_dat.save()
                    new_dat.times_total = 4
                    new_dat.save()
                    continue
                elif(ans_gvn==0):
                    new_dat.times_yes = 1
                    new_dat.save()
                    new_dat.times_total = 4
                    new_dat.save()
                    continue
                elif(ans_gvn==1):
                    new_dat.times_yes = 3
                    new_dat.save()
                    new_dat.times_total = 4
                    new_dat.save()
                    continue
                else:
                    assert(0)
            else:
                new_dat.times_yes = 1
                new_dat.save()
                new_dat.times_total = 2
                new_dat.save()
                continue
    return
    #

# Create your views here.
def intro(request):
    template = 'akinator/intro.html'
    context = {}
    return(render(request, template, context))

def game(request):
    if(request.method=='POST'):
        # obtain users answer
        ans_str = request.POST['answer']
        answer=0
        if(ans_str=='Y'): answer=1
        elif(ans_str=='N'): answer=0
        elif(ans_str=='D'): answer=-1
        else: assert(0)
        # If the user didn't know the answer, request.POST['answer'] is 'D', which is dealt in a while

        # setting current time
        current_time = seconds()

        # cleaning up older ips
        for user in User.objects.all():
            if(abs(current_time-int(user.time_active)) > 300):
                user.delete()

        # obtaining requested ip AND updating the database
        ip_requested = (request.META['HTTP_X_FORWARDED_FOR']).strip()
        flag = False
        user_pk = 0
        for user in User.objects.all():
            if(user.ip_address == ip_requested):
                user.time_active = str(current_time)
                user.save()
                flag = True
                user_pk = user.pk
                break
        if(not(flag)):
            request.method = 'GET'
            return(intro(request))
        currUser = User.objects.get(pk=user_pk)

        # Obtaining the problist data
        prob_of_person = {}  # as in prob_of_person[mukesh's pk] = 0.32
        for probdat in (User.objects.get(pk=user_pk)).prob_list.split('/'):
            prob_of_person[int(probdat.split(',')[0])] = float(probdat.split(',')[1])
        
        # If an answer has already been made give the next question page
        if((((currUser.history.strip('/')).split('/'))[-1]).count(',')>=1):
            request.method = 'GET'
            return(game(request))
        # Updating history with users answer and obtaining the last asked question from it
        currUser.history += (','+str(answer))
        currUser.save()
        last_question_pk = int((((((currUser).history).split('/'))[-1]).split(','))[0])
        
        # Updating the prob_list data based on main algo
        # Note that if the answer is -1 (when the user doesn't know) prob_list_updated does not change
        if(answer!=-1):
            currUser.prob_list = prob_list_updated(prob_of_person, last_question_pk, answer)
            currUser.save()

        # redirecting the page after all the changes had been made
        request.method = 'GET'
        return(game(request))
        
    elif(request.method=='GET'):
        # setting current time
        current_time = seconds()

        # cleaning up older ips
        for user in User.objects.all():
            if(abs(current_time-int(user.time_active)) > 300):
                user.delete()

        # obtaining requested ip AND updating the database
        ip_requested = (request.META['HTTP_X_FORWARDED_FOR']).strip()
        flag = False
        user_pk = 0
        for user in User.objects.all():
            if(user.ip_address == ip_requested):
                user.time_active = str(current_time)
                user.save()
                flag = True
                user_pk = user.pk
                if(user.history.split('/')[-1].count(',')==0):
                    hist = user.history.split('/')
                    hist.pop()
                    user.history = '/'.join(hist)
                    user.save()
                break
        if(not(flag)):
            new_user = User(ip_address=ip_requested, time_active=str(current_time),prob_list=prob_list_new(), history='')
            new_user.save()
            user_pk = new_user.pk
        currUser = User.objects.get(pk=user_pk)

        # obtaining the problist data
        prob_of_person = {}  # as in prob_of_person[mukesh] = 0.32
        for probdat in (currUser.prob_list).split('/'):
            prob_of_person[int(probdat.split(',')[0])] = float(probdat.split(',')[1])

        # picking the best question based on main algo
        remaining_questions = set()
        for a_ques in Question.objects.all():
            remaining_questions.add(a_ques.pk)
        if(len(currUser.history)!=0):
            for used_ques_pk in [int((x.split(','))[0]) for x in ((currUser.history).strip('/')).split('/')]:
                remaining_questions.remove(used_ques_pk)
        new_ques_pk = best_question_pk(prob_of_person, remaining_questions)

        # checking if it is time to end this- based on the problist and size(history)
        flag2 = [False]
        for person in prob_of_person:
            if(prob_of_person[person]>0.5):
                flag2[0] = True
                flag2.append(person)
        # checking if someone has exceeded 60% probablity and getting the hishest probablity person
        maxProbMembers_pks = []
        maxProb = max(list(prob_of_person.values()))
        for memberPk in prob_of_person:
            if(abs(prob_of_person[memberPk]-maxProb)<5e-3):
                maxProbMembers_pks.append(memberPk)
        # checking if max limit of questions has exceeded   
        flag3 = (len((currUser.history.strip('/')).split('/'))>=12)
        # checking if further narrowing down is not possible with the available questions
        flag4 = False
        if(len(currUser.history)!=0):
            flag4 = (new_ques_pk in set([int((x.split(','))[0]) for x in ((currUser.history).strip('/')).split('/')]))
        # checking against don't know button expolitaion for multiple answers
        flag5 = (maxProb>0.21)

        if(flag2[0] or flag3 or flag4):
            # serve the result page
            result_pks = [] # pk of the guys suggested as the answer by the algorithm
            if(flag2[0]):
                result_pks = [flag2[-1]]
            elif(flag3 or flag4):
                if(flag5):
                    result_pks = list(maxProbMembers_pks)
                else:
                    result_pks = [maxProbMembers_pks[0]]
            else:
                assert(0)
            template = 'akinator/result_page.html'
            ansMembersNames = []
            for an_ans_mem_pk in result_pks:
                ansMembersNames.append(' '.join(Member.objects.get(pk=an_ans_mem_pk).member_name.split('.')))
            final_names_string = ', '.join(ansMembersNames)
            message = ''
            if(not(flag5)):
                message = "but like less than "+str(round((maxProb)*100))+"% sure"
            elif(flag2[0]):
                message = get_message(ansMembersNames)
            else:
                if(len(ansMembersNames)>1):
                    message = "'Corporate needs you to find the difference between these people' - 'Algorithm: They are they same'"
                else:
                    message = get_message(ansMembersNames)
            context = {'final_names_string': final_names_string, 'message': message}
            print(final_names_string)
            print(message)
            # delete the user before giving the answer
            # Setting the ans_given for the user
            currUser.ans_given = '.'.join([str(x) for x in result_pks])
            currUser.save()
            return(render(request, template, context))

        # adding that question to the history
        currUser.history += ('/'+str(new_ques_pk))
        currUser.save()

        # rendering the page after the new question is decided
        new_question = (Question.objects.get(pk=new_ques_pk)).question_text
        template = 'akinator/question_page.html'
        question_number = str(len(((currUser.history).strip('/')).split('/')))
        context = {'new_question': new_question,'question_number': question_number}
        return(render(request, template, context))

def submit(request):
    if(request.method=='GET'):
        return(intro(request))
    elif(request.method=='POST'):
        # setting current time
        current_time = seconds()

        # cleaning up older ips
        for user in User.objects.all():
            if(abs(current_time-int(user.time_active)) > 300):
                user.delete()

        # obtaining requested ip AND updating the database
        ip_requested = (request.META['HTTP_X_FORWARDED_FOR']).strip()
        flag = False
        user_pk = 0
        for user in User.objects.all():
            if(user.ip_address == ip_requested):
                user.time_active = str(current_time)
                user.save()
                flag = True
                user_pk = user.pk
                break
        if(not(flag)):
            request.method = 'GET'
            return(intro(request))

        currUser = User.objects.get(pk=user_pk)

        # executed when a name is selected by the user from the select_name_page page
        if('selected_name' in request.POST):
            selected_name = request.POST['selected_name']
            update(selected_name, currUser.history, currUser.ip_address, 0)
            currUser.delete()
            return(intro(request))
        elif('submitted_name' in request.POST):
            submitted_name = request.POST['submitted_name']
            update(submitted_name, currUser.history, currUser.ip_address, 0)
            currUser.delete()
            return(intro(request))

        # if the user says yes
        if(request.POST['answer']=='Y'):
            # if a single answer was given data is saved directly
            if(len(currUser.ans_given.split('.'))==1):
                update(Member.objects.get(pk=int(currUser.ans_given)).member_name, currUser.history, currUser.ip_address, 1)
                currUser.delete()
                return(intro(request))
            # if multiple answers were given, the select_name_page page is rendered
            else:
                template = 'akinator/select_name_page.html'
                the_names = [Member.objects.get(pk=int(x)).member_name for x in currUser.ans_given.split('.')]
                the_names_json = json.dumps(the_names)
                context = {'the_names_json': the_names_json}
                return(render(request, template, context))
        # if the user says no
        elif(request.POST['answer']=='N'):
            # # if the user is not credible, the data is not saved
            # if(max([float((x.split(','))[1]) for x in (currUser.prob_list.strip('/')).split('/')])<=0.21):
            #     # currUser.delete()
            #     return(intro(request))
            # # if the user is credible, submit_name_page page is rendered
            # else:
            if(1):
                template = 'akinator/submit_name_page.html'
                names = []
                for name in Name.objects.all():
                    names.append(name.name_text)
                all_names = json.dumps(names)
                context = {'all_names': all_names}
                return(render(request, template, context))
        else:
            assert(0)
    else:
        assert(0)

def find(request):
    template = 'akinator/find_page.html'
    names = []
    for name in Name.objects.all():
        names.append(name.name_text)
    all_names = json.dumps(names)
    context = {'all_names': all_names}
    return(render(request, template, context))

def fastgame(request):
    if(request.method=='GET'):
        template = 'akinator/fastgame.html'
        #
        member_pk = []
        member_member_name = []
        member_times_searched = []
        #
        question_pk = []
        question_question_text = []
        #
        data_pk = []
        data_times_yes = []
        data_times_total = []
        data_member_pk = []
        data_question_pk = []
        #
        for x in Member.objects.all():
            member_pk.append(x.pk)
            member_member_name.append(x.member_name)
            member_times_searched.append(x.times_searched)
        for x in Question.objects.all():
            question_pk.append(x.pk)
            question_question_text.append(x.question_text)
        for x in Data.objects.all():
            data_pk.append(x.pk)
            data_times_yes.append(x.times_yes)
            data_times_total.append(x.times_total)
            data_member_pk.append(x.member.pk)
            data_question_pk.append(x.question.pk)
        #-----
        mp = json.dumps(member_pk)
        mts = json.dumps(member_times_searched)
        #
        qp = json.dumps(question_pk)
        qqt = json.dumps(question_question_text)
        #
        dp = json.dumps(data_pk)
        dty = json.dumps(data_times_yes)
        dtt = json.dumps(data_times_total)
        dmp = json.dumps(data_member_pk)
        dqp = json.dumps(data_question_pk)
        #-----
        context={'mp':mp, 'mts':mts, 'qp':qp, 'qqt':qqt, 'dp':dp, 'dty':dty, 'dtt':dtt, 'dmp':dmp, 'dqp':dqp}
        return(render(request, template, context))
    
    elif(request.method=='POST'):
        # The result page is rendered and a new user is saved NOW
        
        if(('rpks' in request.POST) and ('history' in request.POST) and ('flags' in request.POST) and ('maxprob' in request.POST)):
            # query data is retrieved
            result_pks = [int(x) for x in request.POST['rpks'].split('.')]
            hist = request.POST['history'].strip()
            maxProb = float(request.POST['maxprob'])
            flags = [int(x) for x in request.POST['flags'].split('.')]
            flag5 = (5 in flags)
            flag2 = [2 in flags]
            
            # first the user is updated/created
            current_time=seconds()
            ip_requested = (request.META['HTTP_X_FORWARDED_FOR']).strip()
            flag = False
            user_pk = 0
            for user in User.objects.all():
                if(user.ip_address == ip_requested):
                    user.time_active = str(current_time)
                    user.history = hist
                    user.save()
                    flag = True
                    user_pk = user.pk
                    break
            if(not(flag)):
                new_user = User(ip_address=ip_requested, history=hist, ans_given=request.POST['rpks'], time_active=str(current_time))
                new_user.save()
                user_pk = new_user.pk            
            
            template = 'akinator/result_page.html'
            ansMembersNames = []
            for an_ans_mem_pk in result_pks:
                ansMembersNames.append(' '.join(Member.objects.get(pk=an_ans_mem_pk).member_name.split('.')))
            final_names_string = ', '.join(ansMembersNames)
            message = ''
            if(not(flag5)):
                message = "but like less than "+str(round((maxProb)*100))+"% sure"
            elif(flag2[0]):
                message = get_message(ansMembersNames)
            else:
                if(len(ansMembersNames)>1):
                    message = "'Corporate needs you to find the difference between these people' - 'Algorithm: They are they same'"
                else:
                    message = get_message(ansMembersNames)
            context = {'final_names_string': final_names_string, 'message': message}
            print(final_names_string)
            print(message)
            return(render(request, template, context))
        else:
            assert(0)
            return(HttpResponse(''))
    else:
        assert(0);
