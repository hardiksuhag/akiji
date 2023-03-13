def get_best_question_pk(prob_context, prob_yes_dat, questions):
    score = {}
    for ques_pk in questions:
        pogo = 0 # probablity of getting one
        for member_pk in prob_yes_dat:
            pogo += (prob_context[member_pk])*(prob_yes_dat[member_pk][ques_pk])
        score[ques_pk] = abs(0.5 - pogo)
    min_score = min(list(score.values()))
    for ques_pk in score:
        if((score[ques_pk]-min_score)<(1e-4)):
            return(ques_pk)
    return(-1)
