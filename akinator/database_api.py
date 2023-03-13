from akinator.models import Name, User, Member, Question, Data
import math
print('Available Functions:')
options=(['create_question','add_names','view_name','check_name','view_question','view_data','get_similar','top(x)',
          'new_question'])
for option in options:
    print(option)
def search(name_list, name_searched, count):
    def dist(a,b,i):
        ans=10
        p1=i
        p2=i
        b1=False
        b2=False
        while(0<=p1<len(b)):
            if(a[i]==b[p1]):
                break
            p1-=1
        while(0<=p2<len(b)):
            if(a[i]==b[p2]):
                break
            p2+=1
        b1=(0<=p1<len(b))
        b2=(0<=p2<len(b))
        if(b1 and b2):
            return(min(abs(p1-i),abs(p2-i)))
        elif(b1 and (not b2)):
            return(abs(p1-i))
        elif((not b1) and b2):
            return(abs(p2-i))
        else:
            return(-1)
    def f(x):
        smth=(math.e)**(x)
        return((smth)/((1+smth)**2))
    def score(test_name_taken):
        test_names_all=test_name_taken.split('.')
        scr_final=0
        for test_name in test_names_all:
            a=[]
            b=[]
            a.extend(name_searched.lower())
            b.extend(test_name.lower())
            scr=0
            for i in range(len(a)):
                d=dist(a,b,i)
                if(d==-1):
                    continue
                else:
                    scr+=f(d)
            scr/=len(a)
            scr_final=max(scr_final,scr)
        return(scr_final)
    name_list.sort(key=score)
    name_list.reverse()
    return(name_list[0:count])

def create_question():
    print('TIP: Construct the question in a way that it says no for more people')
    print('Modes:')
    print('1 for automatic insertion')
    print('2 for manual insertion (choose this only if answer is yes for a small set of people)')
    print('-1 for exiting the API')
    print("Select mode for adding quesion:")
    mode = int(input())
    if(mode==1):
        print('Enter question text:')
        ques_txt = input()
        answers = {}  # answers[member_pk] = 0/1/404
        print('Now enter the answers for all members (0/1 for n/y and 404 if you dont know):')
        print('Enter -1 to exit at any point')
        for member in Member.objects.all():
            ans = int(input('Ans for '+member.member_name+':'))
            if(ans==-1): return
            answers[member.pk] = ans
        new_question = Question(question_text = ques_txt)
        new_question.save()
        for memberPk in answers:
            the_member = Member.objects.get(pk=memberPk)
            new_dat = Data(member=the_member, question=new_question)
            if(answers[memberPk]==0):
                new_dat.times_yes = 1
                new_dat.times_total = 8
                new_dat.save()
            elif(answers[memberPk]==1):
                new_dat.times_yes = 7
                new_dat.times_total = 8
                new_dat.save()
            elif(answers[memberPk]==404):
                new_dat.times_yes = 4
                new_dat.times_total = 8
                new_dat.save()
            else:
                print('Some error occured: Error Code 102')
                print('None of the data you entered was saved')
                print('Do you want to delete the question you just added(0/1)?')
                if(int(input())==1): new_question.delete()
                return
    elif(mode==2):
        print('Enter question text:')
        ques_txt = input()
        print('Now enter the names for which the answer to this question is yes:')
        print('Enter -3 to exit at any point(Nothing gets saved)')
        print('Enter -2 to finish adding')
        all_yes_names = set()
        while(True):
            print('Enter the next name in here:')
            all_names = []
            for member in Member.objects.all():
                all_names.append(member.member_name)
            top_names = search(all_names, input().strip(), 5)
            print('-2: No more names left')
            print('-1: Not in this list')
            for i in range(5): print(str(i)+': '+top_names[i])
            ii = int(input())
            if(ii==-1):
                continue
            elif(ii==-2):
                break
            elif(ii==-3):
                return
            name_txt = top_names[ii]
            all_yes_names.add(name_txt)
        new_question = Question(question_text=ques_txt)
        new_question.save()
        for aMember in Member.objects.all():
            new_dat = Data(member=aMember, question=new_question)
            if((aMember.member_name) in all_yes_names):
                new_dat.times_yes = 7
                new_dat.times_total = 8
                new_dat.save()
            else:
                new_dat.times_yes = 1
                new_dat.times_total = 8
                new_dat.save()
    elif(mode==-1):
        return
    else:
        print('Some error occoured: Error Code 101')
        return

def add_names():
    if(1):
        print('Enter the name in here:')
        all_names = []
        for a_name in Name.objects.all(): all_names.append(a_name.name_text)
        top_names = search(all_names, input().strip(), 5)
        print('-1: Not in this list')
        for i in range(5): print(str(i)+': '+top_names[i])
        ii = int(input())
        if(ii==-1): return
        name_txt = top_names[ii]
        answers = {}  # answers[question_pk] = 0/1/404
        for question in Question.objects.all():
            ans = int(input(question.question_text+':'))
            if(ans==-1): return
            answers[question.pk] = ans
        new_member = Member(member_name = name_txt, times_searched = 3)
        new_member.save()
        for questionPk in answers:
            the_question = Question.objects.get(pk=questionPk)
            new_dat = Data(member=new_member, question=the_question)
            if(answers[questionPk]==0):
                new_dat.times_yes = 1
                new_dat.times_total = 8
                new_dat.save()
            elif(answers[questionPk]==1):
                new_dat.times_yes = 7
                new_dat.times_total = 8
                new_dat.save()
            elif(answers[questionPk]==404):
                new_dat.times_yes = 4
                new_dat.times_total = 8
                new_dat.save()
            else:
                print('Some error occured: Error Code 103')
                print('Do you want to delete the member you just added(0/1)?')
                if(int(input())==1): new_member.delete()
                return

def check_name():
    print('Enter the name in here:')
    all_names = []
    for a_name in Name.objects.all(): all_names.append(a_name.name_text)
    top_names = search(all_names, input().strip(), 5)
    print('-1: Not in this list')
    for i in range(5): print(str(i)+': '+top_names[i])
    ii = int(input())
    if(ii==-1): return
    name_txt = top_names[ii]
    for a_mem in Member.objects.all():
        if(a_mem.member_name==name_txt):
            print('Yes')
            return
    print('No')
    return

def view_name():
    print('Enter the name in here:')
    all_names = []
    for a_name in Name.objects.all(): all_names.append(a_name.name_text)
    top_names = search(all_names, input().strip(), 5)
    print('-1: Not in this list')
    for i in range(5): print(str(i)+': '+top_names[i])
    ii = int(input())
    if(ii==-1): return
    name_txt = top_names[ii]
    for a_mem in Member.objects.all():
        if(a_mem.member_name==name_txt):
            print('Times Searched:',a_mem.times_searched)
            break
    for a_dat in Data.objects.all():
        if(a_dat.member.member_name==name_txt):
            print((a_dat.question.question_text)+':'+str(round((int(a_dat.times_yes)/int(a_dat.times_total))*(100)))+'%')

def view_question():
    print('put -1 to exit')
    print(('-'*20))
    for a_ques in  Question.objects.all():
        print(a_ques.pk,':'+a_ques.question_text)
    print('-'*20)
    print('Only those names will be shown whose probablity is more than 50%')
    print('Enter 1234567 to view otherwise:')
    only_no = (input()=='1234567')
    print('Now enter the question ID')
    ii = int(input())
    if(ii==-1): return
    ques_pk = ii
    if(not(only_no)):
        for a_dat in Data.objects.all():
            if(a_dat.question.pk==ques_pk and (round((int(a_dat.times_yes)/int(a_dat.times_total))*(100))>50)):
                print((a_dat.member.member_name)+':'+str(round((int(a_dat.times_yes)/int(a_dat.times_total))*(100)))+'%')
    else:
        for a_dat in Data.objects.all():
            if(a_dat.question.pk==ques_pk and (round((int(a_dat.times_yes)/int(a_dat.times_total))*(100))<=50)):
                print((a_dat.member.member_name)+':'+str(round((int(a_dat.times_yes)/int(a_dat.times_total))*(100)))+'%')
                
def view_data():
    print('Enter the name in here:')
    all_names = []
    for a_name in Name.objects.all(): all_names.append(a_name.name_text)
    top_names = search(all_names, input().strip(), 5)
    print('-1: Not in this list')
    for i in range(5): print(str(i)+': '+top_names[i])
    ii = int(input())
    if(ii==-1): return
    name_txt = top_names[ii]
    #
    print(('-'*20))
    for a_ques in  Question.objects.all():
        print(a_ques.pk,':'+a_ques.question_text)
    print('Now enter the question ID (-1 to return)')
    ii = int(input())
    if(ii==-1): return
    ques_pk = ii
    #
    for a_dat in Data.objects.all():
        if(a_dat.member.member_name==name_txt and a_dat.question.pk==ques_pk):
            print(str(round((int(a_dat.times_yes)/int(a_dat.times_total))*(100)))+'%')
            return

# from bisect import bisect_left as ind
def get_name_from_pk(apk):
    return(Member.objects.get(pk=apk).member_name)

def get_similar():
    all_questions = []
    for a_ques in Question.objects.all():
        all_questions.append(a_ques.pk)
    all_members = [] # all_datas[member_pk] = string;
    for a_member in Member.objects.all():
        all_members.append(a_member.pk)
    all_questions.sort()
    all_members.sort()
    # print('all_members',all_members)
    # print('all_questions',all_questions)
    all_datas = {}
    for mem_pk in all_members:
        all_datas[mem_pk] = {}
    for a_data in  Data.objects.all():
        all_datas[int(a_data.member.pk)][int(a_data.question.pk)] = round(float(a_data.times_yes)/float(a_data.times_total))
    member_strings = []
    # print('all_datas[40]',all_datas[40])
    for i in range(len(all_members)):
        mah_str = []
        for j in range(len(all_questions)):
            mah_str.append(all_datas[all_members[i]][all_questions[j]])
        mah_str.append(all_members[i])
        member_strings.append(list(mah_str))
    # print('member_strings[20]',member_strings[20])
    member_strings.sort()
    same_name_groups = []
    i=0
    while(i<len(member_strings)):
        j=i
        while(member_strings[i][0:len(all_questions)]==member_strings[j][0:(len(all_questions))]):
            if(j>i):
                print(Member.objects.get(pk=(member_strings[j][-1])).member_name,member_strings[j][0:len(all_questions)])
            j+=1
            if(j==len(member_strings)):
                break
        if((j-i)>1):
            same_name_groups.append([((get_name_from_pk(x[-1]).split('.'))[0]).lower() for x in member_strings[i:j]])
        i=j
    print(len(same_name_groups))
    for x in same_name_groups:
        print(', '.join(x))

def top(x):
    a=[x for x in Name.objects.all()]
    a.sort(key=(lambda x:(int(x.search_count))), reverse=True)
    for i in range(x): print(a[i].name_text+'-'+a[i].search_count+' searches')
    
def new_question():
    print('Enter -1 to continue')
    print('ENTER QUESTION TEXT:')
    ques_text=input()
    newquestion = Question(question_text=ques_text)
    newquestion.save()
    for mem in Member.objects.all():
        newdata = Data(times_yes=1,times_total=2,member=mem,question=newquestion)
        newdata.save()
    
    
    

    
    
    
    
    
    
    
    
    
    
