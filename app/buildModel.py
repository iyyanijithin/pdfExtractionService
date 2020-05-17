
import os
import pandas as pd

import pandas as pd, numpy as np
from sklearn.naive_bayes import MultinomialNB


from pdfUtil import checkIfPdfIsDigital,getAllTextObj
from appUtil import getStopWords,filterData
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def buildModelExcel():
    print('Reading input pdf files')
    dict1 = {}
    files_list = []
    for root, dirs, files in os.walk(os.path.abspath(os.path.dirname(__file__)) + "\\dataSet\\pdf"):
        for file in files:
            if file.endswith(".pdf"):
                files_list.append(os.path.join(root, file))

    for file in files_list:
        print(file)
        isDigital = checkIfPdfIsDigital(file)
        if isDigital:
            print('Processing digital document')
            textFromPdf = getAllTextObj(file)
            dict1[file] = " ".join(textFromPdf)
          
        else:
            print('Is image pdf')
    #print(dict1)
    df = pd.DataFrame(data=dict1, index=[0])
    df = (df.T)
    df.to_excel(os.path.abspath(os.path.dirname(__file__)) + '\\dataSet\\\inputDataForLabelling.xlsx')
    print('Data from pdf converted to excel')



def buildModelFromExcel():
    print('building model from excel')   
    text_data_df = pd.read_excel(os.path.abspath(os.path.dirname(__file__)) + '\\model\\\dataClassificationModel.xlsx', index_col=[0])
    for i in range(0,len(text_data_df['TEXT'])):
        #Replace new line by space and strip
        text_data_df.iloc[i]['TEXT'] = filterData(text_data_df.iloc[i]['TEXT'])
        #Removing dot(.) from text
        

    #Lemmatization is pending
    print(text_data_df['TEXT'])
    X_train, X_test, y_train, y_test = train_test_split(text_data_df['TEXT'], text_data_df['LABEL'], 
                                                    test_size=0.2)
    print(len(X_train),len(y_train),len(X_test),len(y_test))
    count_vectorizer = CountVectorizer(strip_accents='ascii',lowercase=True, analyzer='word')
    X_train_cv = count_vectorizer.fit_transform(X_train)
    X_test_cv = count_vectorizer.transform(X_test)
    print ('Shape of Sparse Matrix: ', X_train_cv.shape)
    print ('Amount of Non-Zero occurences: ', X_train_cv.nnz)
    print ('sparsity: %.2f%%' % (100.0*X_train_cv.nnz/ (X_train_cv.shape[0] * X_train_cv.shape[1])))
    Features = pd.DataFrame(count_vectorizer.get_feature_names())
    print(Features.head(5))

    #Build model object
    NB_Model = MultinomialNB(alpha=0.01)
    NB_Model.fit(X_train_cv.toarray(), np.array(y_train))
    y_pred = NB_Model.predict(X_test_cv.toarray())
    print(X_test)
    print(y_pred)

    return NB_Model,count_vectorizer

buildModelFromExcel()
