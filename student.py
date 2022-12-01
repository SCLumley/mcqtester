import question
import exam
import random
import copy
import math

class Student:
    def __init__(self,kf=1.0,conf=0.5):
        self.knowledge = kf
        self.confidence = conf
        self.questionMask = []
        self.questionList = []


    def evaluateQuestion(self,question,Elimination):

        questionNumber = self.questionList.index(question)
        rubric = question.question
        evaluation = self.questionMask[questionNumber].question
        qscale = 1/len(rubric)
        reduction = Elimination*qscale

 #       print(questionNumber,qscale,reduction)
 #       print("evaluation before:", evaluation)

        falseAnswers = [k for k, a in rubric.items() if a <= 0]
        unEliminatedAnswers = [k for k, a in evaluation.items() if a > 0]
        answersToEliminate = set(falseAnswers).intersection(set(unEliminatedAnswers))

  #      print("selecting recution from",answersToEliminate)

        falseAnswer = random.choice(list(answersToEliminate))

 #       print("reducing:", falseAnswer)

        #reduce student's evaluation of false answer being true
        evaluation[falseAnswer] -= reduction
        #catch if it gets eliminated
        if evaluation[falseAnswer] < 0:
   #         print("answer fully eliminated")
            reduction += evaluation[falseAnswer]
            evaluation[falseAnswer] = 0
  #          print("actual reduction",reduction)

        #Distribute probability amongst remaining questions:
        newUnEliminatedAnswers = [k for k, a in evaluation.items() if a > 0 and k is not falseAnswer]
        probIncrease = reduction / len(newUnEliminatedAnswers)
        for unEliminatedAnswer in newUnEliminatedAnswers:
            evaluation[unEliminatedAnswer] += probIncrease

 #       print("evaluation after",evaluation)



        return reduction/qscale


    def answerQuestion(self,exam,question):

        questionNumber = self.questionList.index(question)
        rubric = self.questionList[questionNumber].question
        evaluation = self.questionMask[questionNumber].question

        #cases to evaluate

  #      print("answering question", questionNumber)
  #      print(list(evaluation.items()))
  #      print("Best guesses",[(k,a) for k, a in list(evaluation.items()) if a == max(list(evaluation.values()))])
   #     print("consequence", sum([a for k,a in rubric.items() if a <= 0]))
  #      print("Confidenced in possible answers",sum([a for k, a in list(evaluation.items()) if a > 1/len(evaluation)]))
  #      print("risk tolerance:",(1 - self.confidence))

        #1. Student is certain of answer
        if len([a for k, a in list(evaluation.items()) if math.isclose(a, 1.0)]) != 0:
   #          print("student knows answer")
             studentAnswer = [k for k, a in list(evaluation.items()) if math.isclose(a, 1.0)]

        #2. Student is not certain, but there is no penalty, so they will take their best guess
        elif sum([a for k,a in rubric.items() if a <= 0]) >= 0:
 #           print("student Takes best guess with no consequence for failure")
            studentAnswer = random.choice([k for k, a in list(evaluation.items()) if a == max(list(evaluation.values()))])

        #3. Student is not certain, and there is a penalty, but they are confident enough to risk it
        elif [a for k, a in list(evaluation.items()) if a == max(list(evaluation.values()))][0] > (1 - self.confidence):
  #          print("student Takes best guess with consequence for failure")
            studentAnswer = random.choice([k for k, a in list(evaluation.items()) if a == max(list(evaluation.values()))])

        #4. Student is not certain, and there is a penalty, but they are permitted to hedge, and they are willing to do so
        elif question.multipleAnswer and sum([a for k, a in list(evaluation.items()) if a > 1/len(evaluation)]) > (1 - self.confidence) :
   #         print("student hedges guess with consequence for failure")
            studentAnswer = [k for k, a in list(evaluation.items()) if a > 1/len(evaluation)]

        #5. Student is not certain, and will not risk it
        else:  # student doesn't want to risk it
    #        print("student takes no answer")
            studentAnswer = [""]

   #     print("Answering:", studentAnswer)
        exam.addAnswer(questionNumber, studentAnswer)


    def readExam(self,exam:exam.Exam):
        self.questionList = copy.deepcopy(exam.questionList)
        self.questionMask = copy.deepcopy(exam.questionList)
        for question in self.questionMask:
            question.question = dict.fromkeys(question.question, 1/len(question.question))

    def takeExam(self,exam:exam.Exam):
        self.readExam(exam)
        #evaluate answers
        knownFalseAnswers = round(exam.numWrongAnswers() * self.knowledge)
        readAnswers = 0.0
        while readAnswers < knownFalseAnswers:
           # print(readAnswers,knownFalseAnswers)
            for question in self.questionList:
                questionNumber = self.questionList.index(question)
                evaluation = self.questionMask[questionNumber]

                #Small part to ignore re-evaluating questions that have already been solved
                if len([k for k, a in evaluation.question.items() if math.isclose(a, 1.0)]) != 1:
                    knowledge = random.random()
                    readAnswers += self.evaluateQuestion(question,knowledge)

  #      print("post evaluation question mask:")
  #       for question in self.questionMask:
  #           print(question.question)

        #write answers
        for question in self.questionList:
            self.answerQuestion(exam,question)


