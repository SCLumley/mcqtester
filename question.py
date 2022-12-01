from typing import List


###Example protodict:
exampleProtodict = {
    "A" : 0,
    "B" : 0,
    "C" : 0,
    "D" : 1
}

class Question:
    def __init__(self,protodict,multi=False):
        self.question = protodict
        self.multipleAnswer = multi

    def check(self,answer: List[str]):
#        print("comparing:",self.question,answer)
        score = 0
        if answer != [""]:
            if self.multipleAnswer:
                for item in list(self.question.keys()):
                    if item in answer:
                        score += self.question[item]
            else:
                score += self.question[answer[0]]
        return score


