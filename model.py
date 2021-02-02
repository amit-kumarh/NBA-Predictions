#Imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
#from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import datetime
import finalScraper

def trainModel():
    #loading dataset
    data = pd.read_csv('final.csv')

    #Preprocessing
    X = data.drop('Team1Win', axis=1)
    y = data['Team1Win']

    #Splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

    #Scaling
    global sc
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    #Random Forest Classifier
    #rfc = RandomForestClassifier(n_estimators=200)
    #rfc.fit(X_train, y_train)
    #pred_rfc = rfc.predict(X_test)

    #print(classification_report(y_test, pred_rfc))
    #print(confusion_matrix(y_test, pred_rfc))

    #SVM Classifier
    global clf
    clf = svm.SVC()
    clf.fit(X_train, y_train)

    #Neural Network
    #mlpc = MLPClassifier(hidden_layer_sizes=(11,11,11),max_iter=500)
    #mlpc.fit(X_train, y_train)
    #pred_mlpc = mlpc.predict(X_test)

    #print(classification_report(y_test, pred_mlpc))
    #print(confusion_matrix(y_test, pred_mlpc))

def main():
    trainModel()
    today = datetime.datetime.now()
    stats = finalScraper.scrapeStats()
    matchups = pd.read_csv(f'./games/{today.month}{today.day}.csv')
    data = finalScraper.merge(stats)
    data = data.drop(columns=['Team1GP', "Team1W", 'Team1L', 'Team1MIN', 'Team2GP', "Team2W", 'Team2L', 'Team2MIN', 'Team1', 'Team2'], axis=1)
    data = data.apply(pd.to_numeric, errors='ignore')
    results = open(f"./results/{today.month}{today.day}.txt", 'a')
    for row in range(len(data)):
        Xnew = [[]]
        for i in range(0,28):
            Xnew[0].append(data.iloc[row, i])
        Xnew = sc.transform(Xnew)
        ynew = clf.predict(Xnew)
        results.write(f"{matchups.iloc[row, 0]} vs. {matchups.iloc[row, 1]}: {ynew}\n")
        
        
if __name__ == '__main__':
    main()