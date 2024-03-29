import os,sys,re,glob,ipykernel,tweepy,stockmarket,nltk,collections,itertools,pandas as pd,numpy as np,\
        seaborn as sns, yfinance as yf, matplotlib.pyplot as plt, statsmodels.formula.api as smf,\
        statsmodels.api as sm, autoreload, importlib
from pathlib import Path
from string import punctuation 
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
np.random.seed(0)
pd.set_option('display.max_columns', None)

def format_model(df, split):
    
        X = df.loc[:, 'y':]
        X = X.drop(columns=['y']).astype(float)
        X = sm.add_constant(X) # for using sm version w/out r variant

        y = df.loc[:, 'y'].astype(float)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=0)
        
        return X, y, X_train, X_test, y_train, y_test
    

def linear_model(df, split=0.20, summary = True):
    
    X, y, X_train, X_test, y_train, y_test = format_model(df, split)
    
    lm_train = sm.OLS(y_train, X_train).fit()
    test_pred = lm_train.predict(X_test)

    test_rss = np.sum((y_test - test_pred)**2)
    test_mse = test_rss/len(y_test) # equivalent to mean_squared_error(y_test, test_pred)
    test_rmse = np.square(test_mse)

    lm = sm.OLS(y, X).fit()
    if( summary == True ):
        print(f"train rss: {lm_train.ssr}", end="\n")
        print(f"test rss: {test_rss}", end=" ")
        print(f"test mse: {test_mse}", end=" ")
        print(f"test rmse: {test_rmse}")
        print(lm.summary2())
    model = {'lm':lm, 'lm_train':lm_train, 'test_pred':test_pred,\
            'test_rss':test_rss, 'test_mse':test_mse, 'test_rmse':test_rmse}
    return model

def naive_bayes(df, ticker, summary= True):
    df = create_target(day = 5, ticker = ticker )
    X, y, X_train, X_test, y_train, y_test = format_model(df, split=0.2)
    gnb = GaussianNB()
    y_pred_gaussian = gnb.fit(X_train, y_train).predict(X_test)
    counfusion_mtx = confusion_matrix(y_test, y_pred_gaussian)
    tn, fp, fn, tp = counfusion_mtx.ravel()
    
    accuracy = accuracy_score(y_test, y_pred_gaussian)
    f1 = f1_score(y_test, y_pred_gaussian)
    precision = precision_score(y_test, y_pred_gaussian)
    recall = recall_score(y_test, y_pred_gaussian)
    report = classification_report(y_test, y_pred_gaussian)
    
    if( summary == True ):
        print(counfusion_mtx)
        print(f"\nTrue Negative: {tn}, False Positive: {fp}, False Negative: {fn}, True Positive: {tp}\n")
        print(f"accuracy: {accuracy}\nf1: {f1}\nprecision: {precision}\nrecall: {recall}\n\n{report}")
    
    output = (y_pred_gaussian, counfusion_mtx, tn, fp, fn, tp, accuracy, f1, precision, recall, report)
    
    return output

def create_target(df, day = 5, ticker= "SandP_500"):
    '''
    ex day = 5 
    sum(5 days) / 5 compare to each date if current day > last 5 days 
    If True Then 1 Else 0
    '''
    day_avg = df[ticker].shift(periods=-1).rolling(day).sum().div(day) # period = -1 to start from the oldest
    conditional = df[ticker] > day_avg

    try:
        df.insert(loc = 0,
                        column = 'y',
                        value = np.where(conditional, 1, 0) )
    except ValueError:
        print(ticker)
        pass
    return df 