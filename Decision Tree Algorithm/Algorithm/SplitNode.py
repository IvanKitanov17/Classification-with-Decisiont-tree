class SplitNode:

    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

    def get_question(self):
        return self.question

    def get_true_branch(self):
        return self.true_branch

    def get_false_branch(self):
        return self.false_branch
