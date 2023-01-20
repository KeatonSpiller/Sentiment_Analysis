def user_download_helper(userID, group):
    
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
    
    path = f'../data/{group}'
    if not os.path.exists(path):
        os.makedirs(path)
    df_temp.to_csv(path +'/'+ userID +'_twitter.csv',index=False)  
    
def user_download(user_list, group):
    '''
    # Download users within list of usernames and save in a csv under data
    '''
    try:
        for userID in user_list:
            user_download_helper(userID, group)
            print(userID, end=' ')
    except Exception:
        print(f"Invalid user: {userID}")

# infinite user download attempt
# def infinite_user_download_helper(userID, group, oldest_id):
#     if(oldest_id == None):
#         tweets = api.user_timeline(screen_name=userID, 
#                                 # 200 is the maximum allowed count
#                                 count=200,
#                                 include_rts = False,
#                                 trim_user = False,
#                                 tweet_mode = 'extended'
#                                 )
#         all_tweets = []
#         all_tweets.extend(tweets)
#         oldest_id = tweets[-1].id
#     else:
#         all_tweets = []
#     while True:
#         tweets = api.user_timeline(screen_name=userID, 
#                             # 200 is the maximum allowed count
#                             count=200,
#                             include_rts = False,
#                             max_id = oldest_id - 1,
#                             trim_user = False,
#                             tweet_mode = 'extended'
#                             )
#         if len(tweets) == 0:
#             break
#         oldest_id = tweets[-1].id
#         all_tweets.extend(tweets)
#         # print('N of tweets downloaded till now {}'.format(len(all_tweets)))
        
#     regex = "(@[A-Za-z0-9]+)|(\w+:\/\/\S+)"
#     outtweets = []
#     for idx,tweet in enumerate(all_tweets):
#         # encode decode
#         txt = tweet.full_text
#         txt = txt.encode("utf-8").decode("utf-8")
#         # remove @ and website links
#         txt = ' '.join(re.sub(regex, " ", txt).split())
#         # remove punctuation
#         txt = re.sub(f"[{re.escape(punctuation)}]", "", txt)
#         # remove non characters
#         txt = re.sub(f"([^A-Za-z0-9\s]+)", "", txt)
#         # store as a string
#         txt = " ".join(txt.split())
#         tweet_list = [
#         tweet.id_str,
#         tweet.created_at,
#         tweet.favorite_count, 
#         tweet.retweet_count,
#         'https://twitter.com/i/web/status/' + tweet.id_str,
#         txt 
#         ]
#         outtweets.append(tweet_list)
#     df_temp = pd.DataFrame(outtweets, columns=['id','created_at','favorite_count',\
#                                                 'retweet_count','url','text'])
    
#     # using dictionary to convert specific columns
#     convert_dict = {'id': 'int64',
#                     'created_at': 'datetime64[ns, UTC]',
#                     'favorite_count': 'int64',
#                     'retweet_count': 'int64',
#                     'url': 'object',
#                     'text': 'object'}
#     df_temp = df_temp.astype(convert_dict)
    
#     path = f'../data/{group}'
#     if not os.path.exists(path):
#         os.makedirs(path)
#     if(os.path.exists(path +'/'+ userID +'_twitter.csv')):
#         df = pd.read_csv(path +'/'+ userID +'_twitter.csv').astype(convert_dict)
#     else:
#         df = pd.DataFrame()
#     print(not df.equals(df_temp))
#     if df_temp not in df:
#         df = pd.concat([df_temp,df], axis = 0, join = 'outer',names=['id','created_at','favorite_count',\
#                                                                      'retweet_count','url','text']).astype(convert_dict)
#         df.to_csv(path +'/'+ userID +'_twitter.csv',index=False)
#     else:
#         print('duplicates exist')
        
#     oldest_date = df.created_at.min()
#     # newest_date = df.created_at.max()
    
#     return oldest_id, oldest_date
        
# def infinite_user_download(user_list, group):
#     try:
#         for userID in user_list:
#             oldest_id, oldest_date = infinite_user_download_helper(userID, group, oldest_id=None)
#             for i in range(0,3):
#                 oldest_id, oldest_date = infinite_user_download_helper(userID, group, oldest_id)
#             print(f'{userID}: {i+1} iterations', end=' ')
#     except Exception:
#         print(f"Invalid user: {userID}")
        
# infinite_user_download(['jimcramer'], 'test') 

def merge_files(group, display):
    csv_files = glob.glob(os.path.join('../data'+"/"+group, "*.csv"))
    df = pd.DataFrame()
    convert_dict = {'id': 'int64',
                        'created_at': 'datetime64[ns, UTC]',
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
    path_group_merge = f'../data/{group}/merge/'
    path_merge = f'../data/merge/merged_twitter_analysts/'
    if not os.path.exists(path_group_merge):
        os.makedirs(path_group_merge)
    if not os.path.exists(path_merge):
        os.makedirs(path_merge)
    df.to_csv(path_group_merge +'/merged_'+ group +'.csv',index=False)
    df.to_csv(path_merge +'/merged_'+ group +'.csv',index=False)

    return df 

def merge_all(group, display):
    
    csv_files = glob.glob(os.path.join('../data'+"/"+group, "*.csv"))
    df = pd.DataFrame()
    convert_dict = {'id': 'int64',
                        'created_at': 'datetime64[ns, UTC]',
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
    path_merge = f'../data/merge/all_merged_twitter_analysts'
    if not os.path.exists(path_merge):
        os.makedirs(path_merge)
    df.to_csv(path_merge +'/all_merged_twitter_analysts.csv',index=False)
    
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