import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


nombre="Zoologicos Ordenado";    


with open("ordenados/"+nombre+".csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count = 0
    reviews_train = []
    reviews_test = []

    todo = []
    ctotal=0
    positivo = []
    cpositivo = 0
    negativo = []
    cnegativo=0
    
    #condicion=True;
    for row in csv_reader:
        #print(line_count)
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
          todo.append(row[3].strip())
          if(float(row[4])>3.5):
            positivo.append(row[3].strip())
            line_count += 1
          elif (float(row[4])<=3.5):
            negativo.append(row[3].strip())
            line_count += 1
    
    """
    Para Baños, 
    hay 2368 comentarios. 195 menores a 3.5 y 2173 mayores a 3.5
    """   
    cpositivo= len(positivo);  
    cnegativo= len(negativo); 
    ctotal=line_count-1; 
    print("Comentarios posiivos: ",cpositivo);
    print("Comentarios negativos: ",cnegativo);
    print("Comentarios totales: ",ctotal)       
    
    reviews_train = todo;
    reviews_test = todo;

    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    NO_SPACE = ""
    SPACE = " "

    def preprocess_reviews(reviews):
        
        reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
        
        return reviews

    reviews_train_clean = preprocess_reviews(reviews_train)
    reviews_test_clean = preprocess_reviews(reviews_test)

    """
    , ngram_range=(1, 2)
    """

    cv = CountVectorizer(binary=True)
    cv.fit(reviews_train_clean)
    X = cv.transform(reviews_train_clean)
    X_test = cv.transform(reviews_test_clean)

    target = [1 if i < cpositivo else 0 for i in range(ctotal)]

    X_train, X_val, y_train, y_val = train_test_split(
        X, target, train_size = 0.75
    )
    mayorProb=0
    mayorC=0;
    for c in [0.01, 0.05, 0.25, 0.5, 1]:
        
        lr = LogisticRegression(C=c)
        lr.fit(X_train, y_train)
        print ("Accuracy for C=%s: %s" 
              % (c, accuracy_score(y_val, lr.predict(X_val))))
        if(accuracy_score(y_val, lr.predict(X_val))>mayorProb):
          mayorProb=accuracy_score(y_val, lr.predict(X_val));
          mayorC=c;
    """
    para baños
    Accuracy for C=0.01: 0.9054054054054054
    Accuracy for C=0.05: 0.9054054054054054
    Accuracy for C=0.25: 0.9087837837837838
    Accuracy for C=0.5: 0.9087837837837838 ELEGIDA
    Accuracy for C=1: 0.9070945945945946
    """

    print("C escogido de: ", mayorC, " con probabilidad de: ", mayorProb)   

    final_model = LogisticRegression(C=mayorC)
    final_model.fit(X, target)
    print ("Final Accuracy: %s" 
          % accuracy_score(target, final_model.predict(X_test)))

    feature_to_coef = {
        word: coef for word, coef in zip(
            cv.get_feature_names(), final_model.coef_[0]
        )
    }
    for best_positive in sorted(
        feature_to_coef.items(), 
        key=lambda x: x[1], 
        reverse=True)[:50]:
        print (best_positive)
        
    #     ('excellent', 0.9288812418118644)
    #     ('perfect', 0.7934641227980576)
    #     ('great', 0.675040909917553)
    #     ('amazing', 0.6160398142631545)
    #     ('superb', 0.6063967799425831)
        
    for best_negative in sorted(
        feature_to_coef.items(), 
        key=lambda x: x[1])[:50]:
        print (best_negative)




with open("ordenados/"+nombre+".csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count = 0
    reviews_train = []
    reviews_test = []

    todo = []
    ctotal=0
    positivo = []
    cpositivo = 0
    negativo = []
    cnegativo=0
    
    #condicion=True;
    for row in csv_reader:
        #print(line_count)
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
          todo.append(row[3].strip())
          if(float(row[4])>3.5):
            positivo.append(row[3].strip())
            line_count += 1
          elif (float(row[4])<=3.5):
            negativo.append(row[3].strip())
            line_count += 1
    
    """
    Para Baños, 
    hay 2368 comentarios. 195 menores a 3.5 y 2173 mayores a 3.5
    """   
    cpositivo= len(positivo);  
    cnegativo= len(negativo); 
    ctotal=line_count-1; 
    print("Comentarios posiivos: ",cpositivo);
    print("Comentarios negativos: ",cnegativo);
    print("Comentarios totales: ",ctotal)       
    
    reviews_train = todo;
    reviews_test = todo;

    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    NO_SPACE = ""
    SPACE = " "

    def preprocess_reviews(reviews):
        
        reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
        
        return reviews

    reviews_train_clean = preprocess_reviews(reviews_train)
    reviews_test_clean = preprocess_reviews(reviews_test)



    cv = CountVectorizer(binary=True, ngram_range=(1, 2))
    cv.fit(reviews_train_clean)
    X = cv.transform(reviews_train_clean)
    X_test = cv.transform(reviews_test_clean)

    target = [1 if i < cpositivo else 0 for i in range(ctotal)]

    X_train, X_val, y_train, y_val = train_test_split(
        X, target, train_size = 0.75
    )
    mayorProb=0
    mayorC=0;
    for c in [0.01, 0.05, 0.25, 0.5, 1]:
        
        lr = LogisticRegression(C=c)
        lr.fit(X_train, y_train)
        print ("Accuracy for C=%s: %s" 
              % (c, accuracy_score(y_val, lr.predict(X_val))))
        if(accuracy_score(y_val, lr.predict(X_val))>mayorProb):
          mayorProb=accuracy_score(y_val, lr.predict(X_val));
          mayorC=c;
    """
    para baños
    Accuracy for C=0.01: 0.9054054054054054
    Accuracy for C=0.05: 0.9054054054054054
    Accuracy for C=0.25: 0.9087837837837838
    Accuracy for C=0.5: 0.9087837837837838 ELEGIDA
    Accuracy for C=1: 0.9070945945945946
    """

    print("C escogido de: ", mayorC, " con probabilidad de: ", mayorProb)   

    final_model = LogisticRegression(C=mayorC)
    final_model.fit(X, target)
    print ("Final Accuracy: %s" 
          % accuracy_score(target, final_model.predict(X_test)))

    feature_to_coef = {
        word: coef for word, coef in zip(
            cv.get_feature_names(), final_model.coef_[0]
        )
    }
    for best_positive in sorted(
        feature_to_coef.items(), 
        key=lambda x: x[1], 
        reverse=True)[:50]:
        print (best_positive)
        
    #     ('excellent', 0.9288812418118644)
    #     ('perfect', 0.7934641227980576)
    #     ('great', 0.675040909917553)
    #     ('amazing', 0.6160398142631545)
    #     ('superb', 0.6063967799425831)
        
    for best_negative in sorted(
        feature_to_coef.items(), 
        key=lambda x: x[1])[:50]:
        print (best_negative)


    