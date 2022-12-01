import copy

import question

class Exam:
    def __init__(self):
        self.questionList=[]
        self.studentAnswers=[]
        self.mark = 0

    def addQuestion(self,protodict:dict,qty=1,multi=False):
        for _ in range(qty):
            newQuestion = question.Question(protodict,multi)
            self.questionList.append(copy.deepcopy(newQuestion))
            self.studentAnswers.append([""])

    def readQuestion(self,questionNumber=0):
        return self.questionList[questionNumber]

    def numQuestions(self):
        return len(self.questionList)

    def numAnswers(self):
        total = 0
        for q in self.questionList:
            total += len(q.question)
        return total

    def numWrongAnswers(self):
        total = 0
        for q in self.questionList:
            total += len( {k: a for k, a in q.question.items() if a <= 0} )
        return total

    def numRightAnswers(self):
        total = 0
        for q in self.questionList:
            total += len( {k: a for k, a in q.question.items() if a > 0} )
        return total

    def addAnswer(self,questionNumber=0,studentAnswer=[""]):
        self.studentAnswers[questionNumber]=studentAnswer

    def markPaper(self):
        self.mark = 0
        for q, a in zip(self.questionList, self.studentAnswers):
            self.mark += q.check(a)



