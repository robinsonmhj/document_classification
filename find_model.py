import logging.config
import yaml

import pandas as pd
from pandas import DataFrame
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


from file_procsser import separateData

logger = logging.getLogger(__name__)
def get_best_algorithm(categories, tfidf, cv=10):
    """
    @brief given the data and find out the best algorithm 
    @param categories it is a list which contains the label of a document
    @param documents, the tfidf data which are preprocessed 
    @param cv, the number of cross validation
    
    """
    models = [
#               RandomForestClassifier(n_estimators=200,max_depth=3, random_state=0),
#               MultinomialNB(),
#               KNeighborsClassifier(n_neighbors=10),
              SGDClassifier(random_state=0),
              LogisticRegression(random_state=0)]
    
    entries = []
    df = pd.DataFrame(index=range(cv*len(models)))
    for model in models:
        model_name = model.__class__.__name__
        logger.info("{} starts".format(model_name))
        accuracies = cross_val_score(model, tfidf, categories, scoring="accuracy", cv=cv)
        for fold_id, accuracy in enumerate(accuracies):
            entries.append((model_name , fold_id, accuracy))
        
    df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    logger.info(df)
    
    return df.loc[df['accuracy'].idxmax()]['model_name']


def get_best_params(categories, documents, params, pipeline, cv=5):
    """
        @brief get the params for the best accuracy model
        @param categories, category list for the documents
        @param documents, a list of document
        @param params, the range of params to try
        @param pipeline, model pipeline
    
    """
    
    logger.info("start to find the best params")
    gs = GridSearchCV(pipeline, params, cv=cv)
    gs = gs.fit(documents, categories)
    logger.info("Finished finding the best params")
    for param_name in sorted(params.keys()):
        logger.info("{}:{}".format(param_name, gs.best_params_[param_name]))
        return (gs.best_score_,param_name,gs.best_params_[param_name])


def find_best_model_parameter():
    for i in range(20,1,-1):
        msg = "{} splits".format(i)
        logger.info(msg)
        file_name = "/home/robin/Downloads/shuffled-full-set-hashed.csv"
        data1,data2 = separateData(i, file_name)
        df = DataFrame(data1[0])
        category = pd.factorize(df.get(0))[0]
        contents = data2[0]
    
        tfidf_vectorizer=TfidfVectorizer(use_idf=True)
        tfidf=tfidf_vectorizer.fit_transform(contents)
        model_name = get_best_algorithm(category, tfidf)
        logger.info("best model is {}".format(model_name))
        
        data1,data2 = separateData(i, file_name)
        category = data1[0]
        contents = data2[0]
        if model_name == "RandomForestClassifier":
            model = RandomForestClassifier()
            continue
        elif model_name == "MultinomialNB":
            model = MultinomialNB()
            continue
        elif model_name == "KNeighborsClassifier":
            model = MultinomialNB(n_neighbors=10)
            continue
        elif model_name == "SGDClassifier":
            model = SGDClassifier(random_state=0)
            parameters = {
                    'classifier__alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3], # learning rate
                    'classifier__n_iter': [20], # number of epochs
                    'classifier__loss': ['log'], # logistic regression,
                    'classifier__penalty': ['l2'],
                    'classifier__n_jobs': [-1]
                }
        elif model_name == "LogisticRegression":
            model = LogisticRegression(random_state=0)
            parameters = {
            "classifier__C":np.logspace(-3,3,7), "classifier__penalty":["l1","l2"]
        }
        logis_pip = Pipeline([
            ('tfidf', TfidfVectorizer(use_idf=True)),
            ('classifier', model)
        ])    

        res = get_best_params(category, contents, parameters, logis_pip)
        logger.info(res)
        
        
if __name__ == "__main__":
    with open('logging.yaml','rt') as f:
        conf=yaml.safe_load(f.read())
        logging.config.dictConfig(conf)
    logger=logging.getLogger(__name__)
    
    find_best_model_parameter()  