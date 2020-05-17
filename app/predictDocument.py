from pdfUtil import getAllTextObj
from appUtil import filterData
import pandas as pd

def classifyDocumentType(NB_Model,count_vectorizer,file):
    docType = "Undefined"
    textFromPdf = getAllTextObj(file) 
    inputText = ''.join(textFromPdf)
    inputText = filterData(inputText)
    series = pd.Series(inputText)   
    test_cv = count_vectorizer.transform(series)
    y_pred = NB_Model.predict(test_cv.toarray())
    print('Prediction is ',y_pred)
    return y_pred

