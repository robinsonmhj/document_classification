import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

import logging.config
import yaml
import os

import pickle


from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from file_procsser import separateData

logger = logging.getLogger(__name__)

def predict(classifier, tfidf_vec, testing_data_file, test_tfidf=None):
    """
        @brief predict the document type 
        @param classifier, the model which used to predict
        @param file, a space separated file
    
    """
    data = []
    if testing_data_file is not None and os.path.exists(testing_data_file):
        with open(testing_data_file,"r") as f:
            for line in f:
                lines = line.split(",")
                data.append(lines[1].replace("\n",""))
        test_tfidf = tfidf_vec.transform(data)

    if test_tfidf is None:
        return ("UKNOWN",0)
    
    classes = classifier.classes_.tolist()
    predicted = classifier.predict(test_tfidf)
    predict_proba = classifier.predict_proba(test_tfidf)
    for prediction,proba_row in zip(predicted,predict_proba):
            return (prediction,round(proba_row[classes.index(prediction)],4))

def load_stored_model():
    pickle_file = "classfier.pickle"
    if os.path.exists(pickle_file):
        logger.info("begin to read pickle file")
        with open(pickle_file,'rb') as hidden_file:
            classifier = pickle.load(hidden_file)
            tfidf_vec = pickle.load(hidden_file)
        logger.info("finished reading pickle file")
    return classifier, tfidf_vec

def train_model(model, category, content):
    """
        @brief get a trained model 
        @param model the model which used to be used
        @df datafram which used to train the model
    
    """
    tfidf_vec = TfidfVectorizer(use_idf=True)
    tfidf = tfidf_vec.fit_transform(content)
    classifier = model.fit(tfidf, category)
    return classifier,tfidf_vec

def predict_direct(testing_data_file, testing_data_list=None, train_model_flag = False, pickle_file="classfier.pickle"):
    if train_model_flag:
        training_file="training_data.csv"
        category, content = separateData(10, training_file)
        model = SGDClassifier(random_state=0,loss='log')
        classifier,tfidf_vec = train_model(model, category[0], content[0])
        with open(pickle_file,'wb+') as hidden_file:
            pickle.dump(classifier, hidden_file)
            pickle.dump(tfidf_vec, hidden_file)
    else:
        with open(pickle_file,'rb') as hidden_file:
            classifier = pickle.load(hidden_file)
            tfidf_vec = pickle.load(hidden_file)
    if testing_data_list is not None:
        tfidf=tfidf_vec.transform(testing_data_list)
    res = predict(classifier, tfidf_vec, testing_data_file, tfidf)
    return res

class ModelPredication:
    
    def __init__(self, pickle_file):
        self.logger = logging.getLogger(self.__class__.__name__)
        with open(pickle_file,'rb') as hidden_file:
            self.classifier = pickle.load(hidden_file)
            self.tfidf_vec = pickle.load(hidden_file)
        self.classes = self.classifier.classes_.tolist()
    
    def predict(self,test_data):
        test_tfidf = self.tfidf_vec.transform(test_data)
        predicted = self.classifier.predict(test_tfidf)
        predict_proba = self.classifier.predict_proba(test_tfidf)
        for prediction,proba_row in zip(predicted,predict_proba):
            return (prediction,round(proba_row[self.classes.index(prediction)],4))

if __name__ == "__main__":
    with open('logging.yaml','rt') as f:
        conf=yaml.safe_load(f.read())
        logging.config.dictConfig(conf)
    logger=logging.getLogger(__name__)
    
#     training_file="training_data.csv"
#     category, content = separateData(5, training_file)
#     
#     with open("smaller_trainning.csv", "w+") as target:
#         for label,feature in zip(category[4],content[4]):
#             target.write("{},{}\n".format(label, feature))
        

    pickle_file = "classfier.pickle"
    mp = ModelPredication(pickle_file)
    data=[]
    data.append("8d21095e8690 b208ae1e8232 4e5019f629a9 a86f2ba617ec 1c3862c83008 f8b0c07e306c f1c9f7517642 377a21b394dc 5071d8aa3768 46c88d9303da 959b4c0a0bb7 d931e701e475 93790ade6682 448cca02dae6 4357c81e10c1 04503bc22789 a31962fbd5f3 1d4249bb404a b61f1af56200 737f89bbbca2 036087ac04f9 b136f6349cf3 c33b5c3d0449 5c4ab6d55c36 caecbc15a560 e67eb757a353 586242498a88 6d25574664d2 e0a08df8ec4c 9cdf4a63deb0 6101ed18e42f b59e343416f7 4e5019f629a9 45238a6f945e 133d46f7ed38 94cfc0229e9f c337a85b8ef9 9f11111004ec f9b20c280980 a9ee836e8303 6bf9c0cb01b4 8fc4ec925d63 c337a85b8ef9 04503bc22789 f0666bdbc8a5 5c02c2aaa67b ef4ba44cdf5f 2b3cd09a5f3f b02eb907dd1a d38820625542 d08444793824 cc9e05bc2a86 746b67da2da6 4a25312439bf fc25f79e6d18 7d9e333a86da ce1f034abb5d 5b023dd25b4b 2d00e7e4d33f 98d0d51b397c fe081ae57a8b fe286bb08719 eeb86a6a04e4 57e641d8b3b5 eb4baad85df9 610915fceac6 ed214114032c 65f888439937 7d9e333a86da c99723547aac 37ba1eb08496 585bc9de3d49 d02e0be86f53 93790ade6682 37ac79620fc6 4357c81e10c1 0f88ca127938 a31962fbd5f3 f11e7777d8b5 b61f1af56200 eb562127f33e 036087ac04f9 f86490d29db0 b136f6349cf3 cc9e05bc2a86 07e7fe209a3b 93c988b67c47 6240cd5376cf e67eb757a353 edd357b65c83 578830762b27 ea51fa83c91c 9cdf4a63deb0 b59e343416f7 04503bc22789 5c02c2aaa67b 1d4249bb404a 4ad52689d690 a024d1e04168 c337a85b8ef9 2d00e7e4d33f b9699ce57810 594fa5190917 b32153b8b30c 6d25574664d2 1015893e384a 33bfc554cf75 1bc29dc7f887 9e931fae0f23 798fe9915030 07c96d6f390e 3c1f7c78e687 d5a8566dd908 aaf38e8aa6d1 80650ef942e3 14156d1fa057 d17504d2c1e7 010bdb69ff0a 6f6729c54a07 ef4ba44cdf5f b02eb907dd1a d38820625542 7d9e333a86da 37ba1eb08496 f77ad3479ff2 73801426ea65 98d0d51b397c 43565b1afa44 05aa4caf0954 77a36cacbb45")
#     res = predict_direct(None, data, train_model_flag= True)
    res = mp.predict(data)
    print(res)


