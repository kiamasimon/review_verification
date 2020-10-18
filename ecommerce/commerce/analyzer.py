# """
# Author: Esteban Cairol
# Text classifier. Binary sentiment text analysis for Amazon's computer reviews
# """
#
# import sys
# import os
# import random
# import numpy as np
# import matplotlib.pyplot as plt
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn import svm
#
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import confusion_matrix
#
# # from sklearn.model_selection import GridSearchCV
# # from sklearn.datasets import load_files
#
#
# path = 'D:/Projects/Python/ml-amazon-reviews/data'
# files = os.listdir(path)
# perc_train = 0.8
#
# # Randomize files
# random.shuffle(files)
#
# samples = []
# labels = []
#
# for file_name in files:
#     if file_name.endswith(".txt"):
#         # print(file_name)
#         test = file_name
#         file = open(os.path.join(path, file_name) ,'r')
#         samples.append(file.read())
#         labels.append(list(file_name)[5]) # remove 'data\' from string
#         file.close()
#
# n_samples = len(samples)
# index_split = int(perc_train*n_samples)
#
# print ("Total samples read: {}".format(n_samples))
#
# train_samples = samples[0:index_split]
# train_labels = labels[0:index_split]
#
# perc_test = 100-perc_train
# test_samples = samples[index_split+1:n_samples]
# test_labels = labels[index_split+1:n_samples]
# # print(train_labels)
# # print(train_samples)
# text_clf = Pipeline([
# 	('vect', TfidfVectorizer(max_df = 0.8,sublinear_tf=True,use_idf=True)),
# 	('clf', svm.LinearSVC(C=1.0)),
# ])
#
#
# print ("Starting fit process...")
# text_clf.fit(X=train_samples, y=train_labels)
#
# print ("Starting prediction...")
# predicted = text_clf.predict(test_samples)
#
#
# # Calculate Accuracy
# print ("Calculating accuracy...")
# accuracy = text_clf.score(test_samples, test_labels)
# print ("Accuracy {}".format(accuracy))
#
# # Confusion Matrix Analysis
# print ("Building confusion matrix...")
# conf = confusion_matrix(test_labels, predicted)
# print ("Confusion Matrix \n {}".format(conf))
# plt.imshow(conf, cmap='binary', interpolation='None')
#
#
# # Manual test
# def manualPredict(review):
#     prediction = text_clf.predict([review])
#     print (prediction)
#     # manualPredict("Product")
#     context = {
#         "prediction": prediction
#     }
#     return context
#
#
