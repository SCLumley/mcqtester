import student
import question
import exam
import random
import copy



N = 1000
passmark = 50
passKnow = 0.5
lower=0.1
upper = 0.99


q1 = {
    "A": 1,
    "B": 0,
    "C": 0,
    "D": 0
}
q1multi = False
q2 = {
    "A": 1,
    "B": -1/4,
    "C": -1/4,
    "D": -1/4,
    "E": -1 / 4
}
q2multi = False
q3 = {
    "A": 1,
    "B": -1/4,
    "C": -1/4,
    "D": -1/4,
    "E": -1/4
}
q3multi = True


if __name__ == '__main__':


    ##Set up exam
    theExam = exam.Exam()

#    theExam.addQuestion(q1, 100,q1multi)
#    theExam.addQuestion(q2, 100,q2multi)
    theExam.addQuestion(q3, 100, q3multi)


    examStack = []
    for _ in range(N):
        examStack.append(copy.deepcopy(theExam))

    #set up students
    cohort = []
    for _ in range(N):
        k = random.random()
        c = random.uniform(lower, upper)
#        print("generating student with K of:", k)
        cohort.append(student.Student(k,c))


    #run exam
    for i, candidate in enumerate(cohort):
        candidate.takeExam(examStack[i])

    #mark exam
    marks=[]
    for i, exam in enumerate(examStack):
        exam.markPaper()
        marks.append([cohort[i].knowledge,cohort[i].confidence,exam.mark])

    print(marks)

    Tp = len([x for x in marks if x[0] > passKnow and x[2] >= passmark])
    Fp = len([x for x in marks if x[0] < passKnow and x[2] >= passmark])
    Tf = len([x for x in marks if x[0] < passKnow and x[2] < passmark])
    Ff = len([x for x in marks if x[0] > passKnow and x[2] < passmark])

    print("True Pass",  Tp / N)
    print("False Pass", Fp / N)
    print("True Fail",  Tf / N)
    print("False Fail", Ff / N)
    print("Sensitivity", Tp/(Tp+Ff))
    print("Specifcity", Tf / (Tf + Fp))


    if True:
        import matplotlib.pyplot as plt
        import numpy as np

        data = np.array(marks)

    #    print(data)

        x = data[:, 0]*100
        y = data[:, 2]
        z = data[:, 1]


        plt.scatter(x, y, c=z)

        plt.axhline(y=passmark, color="black", linestyle="--")
        plt.axvline(x=passKnow*100, color="black", linestyle="-")

        plt.xlabel("Knowledge Factor (%)")
        plt.ylabel("Exam Score (%)")

        plt.text(28, 95, 'False Passes: ' + str(Fp * 100 / N) + '%',size=16,fontweight="bold")
        plt.text(52, 95, 'True Passes: ' + str(Tp * 100 / N) + '%', size=16, fontweight="bold")
        plt.text(52, 20, 'False Fails: ' + str(Ff * 100 / N) + '%', size=16, fontweight="bold")
        plt.text(28, 20, 'True Fails: ' + str(Tf * 100 / N) + '%', size=16, fontweight="bold")
        plt.text(80, 30, 'Sensitivity: ' + str('{:.1f}'.format(Tp/(Tp+Ff) * 100)) + '%', size=16, fontweight="bold")
        plt.text(80, 20, 'Specificity: ' + str('{:.1f}'.format(Tf/(Tf+Fp)* 100)) + '%', size=16, fontweight="bold")

        plt.show()