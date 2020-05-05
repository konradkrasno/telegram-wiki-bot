# from elasticsearch_dsl.connections import connections
# import re
# import numpy as np
# from sklearn.metrics.pairwise import linear_kernel
# import json
# import pickle
#
# lemmatizer = pickle.load(open('tfidf_data//lemmatizer.p', 'rb'))
#
# tfidf = pickle.load(open('tfidf_data/tfidf.p', 'rb'))
# tfidf_matrix = pickle.load(open('tfidf_data/tfidf_matrix.p', 'rb'))
# title_to_modelid = pickle.load(open('tfidf_data/title_to_modelid.p', 'rb'))
# modelid_to_elasticid = pickle.load(open('tfidf_data/modelid_to_elasticid.p', 'rb'))
#
#
# es = connections.create_connection()
#
# if es.ping():
#     print('Connect')
# else:
#     print('It could not connect!')
#
#
# def remove_punctuations(text):
#     text = re.sub('!|"|\$|%|&|\'|\(|\)|\*|,|-|/|:|;|<|=|>|\?|@|\[|\]|\^|_|`|{|}|~|]|\.', ' ', text)
#     return re.sub(r'\s+', ' ', text).strip()
#
#
# def lemmatize_polish(text):
#     return lemmatizer.replace_keywords(text)
#
#
# def process_text(text):
#     with open('tfidf_data/stopwords_pl.json', 'r', encoding='utf8') as file:
#         stopwords = json.load(file)
#
#     text = remove_punctuations(text)
#     text = lemmatize_polish(text)
#     print(text)
#
#     text = text.lower().split()
#     text = [word for word in text if word not in stopwords]
#     print(text)
#
#     return text
#
#
# def get_ids(query):
#     query_processed = process_text(query)
#
#     keys_modelid = [value for key, value in title_to_modelid.items()
#                     if len(set(key.split()) & set(query_processed)) >= 1]
#
#     vector = tfidf.transform([' '.join(query_processed)])
#     matrix = tfidf_matrix[keys_modelid]
#
#     if np.sum(vector) and np.sum(matrix):
#         tfidf_similarities = linear_kernel(vector, matrix).flatten()
#
#         index = np.argsort(-tfidf_similarities)[0]
#         simm = tfidf_similarities[index]
#
#         return {'modelid': keys_modelid[index],
#                 'elasticid': modelid_to_elasticid[keys_modelid[index]],
#                 'similarity': simm}
#
#
# def search(es_object, index_name, show):
#     res = es_object.search(index=index_name, body=show)
#     return res
#
#
def search_text(query):
    pass
#     _id = get_ids(query)
#     if _id:
#         _id = _id['elasticid']
#         print(_id)
#
#         search_object = {'_source': ['text'], 'query': {'match': {'article_id': _id}}}
#         outcome = search(es, 'wiki_pl', json.dumps(search_object))
#         outcome_text = ' '.join(outcome['hits']['hits'][0]["_source"]["text"].split("\n")[1:10])
#         print(outcome_text)
#
#         return outcome_text, _id
#     return None, None
