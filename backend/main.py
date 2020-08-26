import os
import pandas as pd
import uvicorn
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Company, engine, SessionLocal
from code2name import code2name

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

text_list = []
with open("./data/sample_text.csv") as f:
    line = f.readline()
    while line:
        text_list.append(line.split(",")[3].strip())
        line = f.readline()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/company/{code}")
def company_prices(code: str):
    res = get_prices([code])
    return res


@app.get("/word/{word}")
def search_word(word: str, db: Session = Depends(get_db)):
    with open("./data/sample_text.csv") as f:
        line = f.readline()
        code_list = []
        while line:
            if word in line:
                code_list.append(line.split(",")[2])
            line = f.readline()
    res = None
    if len(code_list) > 0:
        code_list = list(set(code_list))
        res = get_prices(code_list)

    return res


@app.get("/topic/{word}")
def search_topic(word: str):
    get_topic([word])


def get_prices(code_list):
    res_code = []
    res_name = []
    for i, code in enumerate(code_list):
        path = os.path.join('./data', 'stock_data', str(code) + '.T.csv')
        if os.path.exists(path):
            if i == 0:
                df = pd.read_csv(path, header=None, index_col=0)
                df = df.loc[:, 6]
                df.index = pd.to_datetime(df.index)
            else:
                tmp = pd.read_csv(path, header=None, index_col=0)
                tmp = tmp.loc[:, 6]
                tmp.index = pd.to_datetime(tmp.index)
                df = pd.concat([df, tmp], axis=1)
            res_code.append(code)
            if int(code) in code2name.keys():
                res_name.append(code2name[int(code)])

    df = df[df.index.year >= 2020]
    if len(df.shape) > 1:
        df = df.pct_change().mean(axis=1).dropna()
    else:
        df = df.pct_change().dropna()
    res = {
        'R': list(df.values),
        'cumR': list(df.cumsum().values),
        'Date': list(df.index.strftime('%Y-%m-%d')),
        'code': res_code,
        'name': res_name
    }
    return res    


import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from corextopic import corextopic as ct
import scipy.sparse as ss

def analyze(text):
    return text.split(':')

vectorizer = CountVectorizer(analyzer=analyze, min_df=10)
doc_word = vectorizer.fit_transform(text_list)
doc_word = ss.csr_matrix(doc_word)
words = list(np.asarray(vectorizer.get_feature_names()))

not_digit_inds = [ind for ind, word in enumerate(words) if not word.isdigit()]
doc_word = doc_word[:, not_digit_inds]
words = [word for ind, word in enumerate(words) if not word.isdigit()]


def get_topic(anchor_words):
    topic_model = ct.Corex(n_hidden=4, seed=0)
    topic_model.fit(doc_word, words=words, anchors=anchor_words, anchor_strength=1000)
    print(topic_model.get_topics(topic=0, n_words=10))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
