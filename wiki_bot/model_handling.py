# from wiki_bot.qa_models import qaClass

# from deeppavlov import build_model, configs
# model_qa_ml = build_model(configs.squad.squad_bert_multilingual_freezed_emb, download=False)


def first_model(context, text):
    pass
    # return model_qa_ml([context], [text])[0][0]


def second_model(context, text):
    pass
    # return qaClass.get_answer_from_text(text=context, question=text)


choose_model = {
    'first': first_model,
    'second': second_model
}
