from simpletransformers.question_answering import QuestionAnsweringModel

model = QuestionAnsweringModel('bert', 'qa_models/',  use_cuda=False)

class QA():
    def __init__(self, model):
        self.model_qa = model
    def get_answer_from_text(self, text, question):
        to_predict = [
            {'context': text,
            'qas': [{'question': question, 'id': '0'}]}]
        return self.model_qa.predict(to_predict)[0]['answer']


qaClass = QA(model)
# qaClass.get_answer_from_text("Od 1929 Wisława Szymborska mieszkała w Krakowie, gdzie debiutowała w 1945 na łamach „Dziennika Polskiego” wierszem Szukam słowa",  'Jakim wierszem debiutowała Szymborska?')
