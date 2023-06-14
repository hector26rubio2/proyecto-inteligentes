from datetime import datetime
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, cross_val_predict, cross_validate, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

from app.models.dtos.modelOptions import ModelOptions

class ModelEnty:
    
    FOLDER_DATAFRAME_TRAINING = './app/documents/dataframeTraining/'
    FOLDER_MODEL ='./app/models/trainModels/'
    def __init__(self,modelType,normalizationType,overUnderfitting,target,allFeatures,features=None,percentTests=None,numberFolds=None,neighbors=None,kernel=None,depth=None,accuracy=0,precision=0,recall=0,f1=0,modelName="",dataset = "",dataframe= None):
        self.modelType = modelType
        self.normalizationType = normalizationType
        self.overUnderfitting = overUnderfitting
        self.target = target
        self.allFeatures = allFeatures 
        self.features = features
        self.percentTests = percentTests
        self.numberFolds = numberFolds
        self.neighbors = neighbors
        self.kernel = kernel
        self.depth = depth
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall 
        self.f1 = f1
        self.modelName = modelName
        self.dataset = dataset
        self.dataframe = dataframe
        
        
    def toDict(self):
        return {
            "modelType": self.modelType,
            "normalizationType": self.normalizationType,
            "overUnderfitting": self.overUnderfitting,
            "target": self.target,
            "allFeatures": self.allFeatures,
            "features": self.features,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "modelName": self.modelName,
            "dataset": self.dataset
        }
    
    def getFeaturesAndTarget(self):
        try:
            if self.dataframe is None:
                return None

            if self.allFeatures:
                X = self.dataframe.drop([self.target], axis=1)
                self.features = list(X.columns)
            else:
                if not self._existsColumnsInDataframe():
                    return None
                X = self.dataframe.loc[:, self.features]
            y = self.dataframe[self.target]

            return X, y
        except Exception as error:
            raise error


    def _existsColumnsInDataframe(self):
        columnsDf = self.dataframe.columns.tolist()
        if all(columna in columnsDf for columna in self.features):
            return True
        return False
    
    def encoderCategoricalColumns(self, dataframe):
        try:
            encoder = LabelEncoder()
            categoricalColumns = dataframe.select_dtypes(include=['object']).columns
            for column in categoricalColumns:
                dataframe[column] = encoder.fit_transform(dataframe[column].astype(str))
            return dataframe
        except Exception as error:
            raise error

    def encoderTarget(self, target):
        try:
            if not pd.api.types.is_numeric_dtype(target):
                encoder = LabelEncoder()
                return encoder.fit_transform(target)
            
            return target
        except Exception as error:
            raise error
        
    def getModelType(self):
        if self.modelType == ModelOptions.logisticRegression.value:
            return LogisticRegression()
        elif self.modelType == ModelOptions.knn.value:
            return KNeighborsClassifier(n_neighbors=self.neighbors)
        elif self.modelType == ModelOptions.linearRegression.value:
            return LinearRegression()
        elif self.modelType == ModelOptions.naiveBayes.value:
            return GaussianNB()
        elif self.modelType == ModelOptions.decisionTrees.value:
            return DecisionTreeClassifier(max_depth=self.depth)
        elif self.modelType == ModelOptions.svm.value:
            return SVC(kernel=self.kernel)
        else:
            return None
        
        
    def normalizationMinmax(self, dataframe):
        try:
            scalar = MinMaxScaler()
            numericalColumns = dataframe.select_dtypes(include=np.number).columns
            dataframe[numericalColumns] = scalar.fit_transform(dataframe[numericalColumns])
            return dataframe
        except Exception as error:
            raise error

    def normalizationStandarScaler(self, dataframe):
        try:
            scalar = StandardScaler()
            numericalColumns = dataframe.select_dtypes(include=np.number).columns
            dataframe[numericalColumns] = scalar.fit_transform(dataframe[numericalColumns])
            return dataframe
        except Exception as error:
            raise error
        
        
    def fitHoldOut(self, model, x_train, x_test, y_train, y_test):
        self._saveDataframeTraining(features= pd.concat([x_train, x_test], axis=0), 
                                        target= pd.concat([y_train, y_test], axis=0))
        model.fit(x_train, y_train)
        self._saveModel(model)
        y_predict= model.predict(x_test)
        self._metrics(y_test=y_test, y_predict= y_predict)

        return self.toDict()

    def crossValidation(self, model, X, y):
        kf = KFold(n_splits=self.numberFolds, shuffle=True)
        cvResults = cross_validate(model, X=X, y=y,scoring=['accuracy', 'precision', 'recall', 'f1'], cv=kf)
        self.accuracy = cvResults['test_accuracy'].mean()
        self.precision = cvResults['test_precision'].mean()
        self.recall = cvResults['test_recall'].mean()
        self.f1 = cvResults['test_f1'].mean()
        self._saveModel(model)
        return self.toDict()


    def _saveModel(self, model):
        try:
            folderPath = os.path.join(self.FOLDER_MODEL, self.modelType)
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            name = f'{self.modelType}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}' 
            pathModel = os.path.join(folderPath,f"{name}.pkl")
            with open(pathModel, 'wb') as f:
                pickle.dump(model, f)
            self.modelName =  name
        except Exception as error:
            raise error
        
        
    def holdOut(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(self.percentTests / 100), random_state=6)
        return X_train, X_test, y_train, y_test



    def _metrics(self, y_test, y_predict):
        try:
            self.accuracy = accuracy_score(y_test, y_predict)
            print("acc: ", self.accuracy)
            self.precision = precision_score(y_test, y_predict)
            print("precc: ", self.precision)
            self.recall = recall_score(y_test, y_predict)
            print("rec: ", self.recall)
            self.f1 = f1_score(y_test, y_predict)
            print("f1:", self.f1)

        except Exception as error:
            raise error
