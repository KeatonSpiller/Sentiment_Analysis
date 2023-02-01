import os,sys,re,glob,ipykernel,tweepy,stockmarket,nltk,collections,itertools,pandas as pd,numpy as np,\
        seaborn as sns, yfinance as yf, matplotlib.pyplot as plt, statsmodels.formula.api as sm
from pathlib import Path
from string import punctuation 
from datetime import date
from sklearn.model_selection import train_test_split
np.random.seed(0)
import os

def user_download_helper(api, userID, group):
    
    tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            trim_user = False,
                            tweet_mode = 'extended'
                            )
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            trim_user = False,
                            tweet_mode = 'extended'
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        # print('N of tweets downloaded till now {}'.format(len(all_tweets)))
        
    regex = "(@[A-Za-z0-9]+)|(\w+:\/\/\S+)"
    outtweets = []
    for idx,tweet in enumerate(all_tweets):
        # encode decode
        txt = tweet.full_text
        txt = txt.encode("utf-8").decode("utf-8")
        # remove @ and website links
        txt = ' '.join(re.sub(regex, " ", txt).split())
        # remove punctuation
        txt = re.sub(f"[{re.escape(punctuation)}]", "", txt)
        # remove non characters
        txt = re.sub(f"([^A-Za-z0-9\s]+)", "", txt)
        # store as a string
        txt = " ".join(txt.split())
        tweet_list = [
        tweet.id_str,
        tweet.created_at,
        tweet.favorite_count, 
        tweet.retweet_count,
        'https://twitter.com/i/web/status/' + tweet.id_str,
        txt 
        ]
        outtweets.append(tweet_list)
    df_temp = pd.DataFrame(outtweets, columns=['id','created_at','favorite_count',\
                                                'retweet_count','url','text'])
    
    # using dictionary to convert specific columns
    convert_dict = {'id': 'int64',
                    'created_at': 'datetime64[ns, UTC]',
                    'favorite_count': 'int64',
                    'retweet_count': 'int64',
                    'url': 'object',
                    'text': 'object'}
    df_temp = df_temp.astype(convert_dict)
    df_temp.created_at = df_temp.created_at.dt.tz_convert('US/Eastern')
    
    path = f'../Sentiment_Analysis/Stock_Market/data/{group}'
    if not os.path.exists(path):
        os.makedirs(path)
    df_temp.to_csv(path +'/'+ userID +'_twitter.csv',index=False)  
    
def user_download(api, user_list, group):
    '''
    # Download users within list of usernames and save in a csv under data
    '''
    try:
        for userID in user_list:
            user_download_helper(api, userID, group)
            print(userID, end=' ')
    except Exception:
        print(f"Invalid user: {userID}")

def merge_files(group, display):
    csv_files = glob.glob(os.path.join('../Sentiment_Analysis/Stock_Market/data'+"/"+group, "*.csv"))
    df = pd.DataFrame()
    convert_dict = {'id': 'int64',
                        'user':'object',
                        'favorite_count': 'int64',
                        'retweet_count': 'int64',
                        'url': 'object',
                        'text': 'object'}
    for f in csv_files:
        # read the csv file
        df_temp = pd.read_csv(f)
        user_row = f.split("\\")[-1].split(".")[0]
        df_temp.insert(2, 'user', user_row)
        df_temp = df_temp.astype(convert_dict)
        if( display > 0):
            display(df_temp.iloc[0:display])
            print(df_temp.shape)
        # Merging columns of groups
        df = pd.concat([df_temp,df], axis = 0, join = 'outer', names=['id','created_at','user','favorite_count',\
                                                                      'retweet_count','url','text']).astype(convert_dict)
        
    print(f"size of merged data sets of {group}: {df.shape}")
    
    # Creating path and saving to csv
    path_group_merge = f'../Sentiment_Analysis/Stock_Market/data/{group}/merge/'
    path_merge = f'../Sentiment_Analysis/Stock_Market/data/merge/merged_twitter_users/'
    if not os.path.exists(path_group_merge):
        os.makedirs(path_group_merge)
    if not os.path.exists(path_merge):
        os.makedirs(path_merge)
    df.to_csv(path_group_merge +'/merged_'+ group +'.csv',index=False)
    df.to_csv(path_merge +'/merged_'+ group +'.csv',index=False)

    return df 

def merge_all(group, display):
    
    csv_files = glob.glob(os.path.join('../Sentiment_Analysis/Stock_Market/data'+"/"+group, "*.csv"))
    df = pd.DataFrame()
    convert_dict = {'id': 'int64',
                        'user':'object',
                        'favorite_count': 'int64',
                        'retweet_count': 'int64',
                        'url': 'object',
                        'text': 'object'}
    for f in csv_files:
        # read the csv file
        df_temp = pd.read_csv(f)
        df_temp = df_temp.astype(convert_dict)
        # using dictionary to convert specific columns
        if( display > 0):
            display(df_temp.iloc[0:display])
            print(df_temp.shape)
        # Merging columns of everything
        df = pd.concat([df_temp,df], axis = 0, join = 'outer',names=['id','created_at','user','favorite_count',\
                                                                     'retweet_count','url','text']).astype(convert_dict)
         
    print(f"size of merged data sets of {group.split('/')[1]}: {df.shape}")
    
    # Creating path and saving to csv
    path_merge = f'../Sentiment_Analysis/Stock_Market/data/merge/all_merged_twitter_users'
    if not os.path.exists(path_merge):
        os.makedirs(path_merge)
    df.to_csv(path_merge +'/all_merged_twitter_users.csv',index=False)
    
    return df

def strip_all_words(df, stop):
    '''
    grab all words from every text file, removing spaces and non nessesary words from stop list
    '''
    s = df.text
    # lowercase
    s = s.str.lower()
    # drop alphabet
    s = s.replace('[\d]+', '',regex=True)
    # remove stop words
    for i in stop :
        s = s.replace(r'\b%s\b'%i, '',regex=True)
    # remove multiple spaces
    s = s.replace('[\s]{2,}', ' ', regex=True)
    s = s.str.split(' ')
    return s

# navigating the all merged text each twitter message for each word and comparing to frequency of word used
def sentence_word_probability(all_word_count, series_text):
    
    d = all_word_count.to_dict()
    keys, values = d.keys(), d.values()
    sentence_list, total_probability, individual_probability = [], [], []
    N = float(len(keys)) # N is the length of every word in the dictionary of all words used
    
    for i, sentence in enumerate(series_text):
        word_freq, freq_dict, prob_dict, probability_value = {}, [], {}, 0.0
        if( type(sentence) == list ):
            for word in sentence:
                if( sentence != ''):
                    if word in keys:
                        total_words = d[word]
                        v = 1/total_words * 100
                        if(word in word_freq):
                            word_freq[word] = word_freq[word] + v
                        else:
                            word_freq[word] = v
                            
                        freq_dict.append(word_freq)
                        
                        if word in prob_dict:
                            prob_dict[word] = prob_dict[word] + (v/N)
                        else:
                            prob_dict[word] = v/N
                        probability_value += v
                else:
                    print(word)
        # p = word / count(individual word) * 100 / len(# of all words)
        sentence_list.append(freq_dict)
        individual_probability.append(prob_dict)
        total_probability.append(probability_value / N)
        
    return sentence_list, total_probability, individual_probability

def normalize_columns(df, columns):
    for c in columns:
        df[c] = (df[c] - df[c].min()) / (df[c].max() - df[c].min())
    return df 

def normalize_columns_target(df, df_original, columns):
    for c in columns:
        df[c] = (df[c] - df_original[c].min()) / (df_original[c].max() - df_original[c].min())
    return df 

def download_todays_test(ticker_df, df_normalized, df_original):
    # Download today's Index funds, and twitter probabilities
    
    column_names = dict(zip(ticker_df.ticker_name, ticker_df.ticker_label))
    column_names['Datetime']='date'
    stock_list = list(ticker_df.ticker_name)
    stock_str = ' '.join( stock_list )
    current_price = yf.download(stock_str, period='1m', interval = '1m', progress=False)['Close']
    current_price = current_price.loc[[str(current_price.index.max())]].reset_index('Datetime').rename(columns= column_names)
    
    convert_dict = dict(zip(ticker_df.ticker_label, ['float64']*len(ticker_df.ticker_label)))
    current_price = current_price.astype(convert_dict)
    current_price.date = current_price.date.dt.date
    current_price = current_price.astype({'date':'datetime64[ns]'}).set_index('date')
    
    todays_data = df_normalized.loc[df_normalized.index == str(current_price.index[0]),:]
    
    todays_test = pd.merge(current_price, todays_data, how='inner', on='date')
    columns = list(ticker_df.ticker_label) + ['favorite_count', 'retweet_count']
    todays_test = normalize_columns_target(todays_test.copy(), df_original.copy(), columns)
    
    return todays_test