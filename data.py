from urllib import response
import requests
import json
import datetime
import time
from pprint import pprint 
import simplejson

backoff_429_recieved = False
after_datetime = int(datetime.datetime(2022,4,1).timestamp())
before_datetime = int(datetime.datetime(2022, 4, 8).timestamp())
    

def add_time(orig, time_seg, segments):
    orig = datetime.datetime.fromtimestamp(orig)
    time_seg = time_seg.lower()
    if time_seg == 'days': new =datetime.timedelta(days=(segments),seconds=1)
    elif time_seg == 'weeks': new = datetime.timedelta(weeks=segments)
    elif  time_seg == 'months': new = datetime.timedelta(days=(segments*31))
    elif time_seg == 'hours': new = datetime.timedelta(hours=segments)
    elif time_seg == 'years': new = datetime.timedelta(days=(segments*365))
    else: new =datetime.timedelta(days=(segments),seconds=1)
    return int((orig+new).timestamp())



def getPostsFromPushshift(subreddits,terms, beginning, end, time_seg, segments):
    """
    Gets posts from the given subreddit for the given time period
    :param subreddits: the subreddits to retrieve posts from
    :param beginning: The unix timestamp of when the posts should begin
    :param end: The unix timestamp of when the posts should end (defaults to right now)
    :return:
    """
    terms = terms.split(",")
    data = []
    full_data = {}
    # convert to a list if necessary
    if not isinstance(subreddits, list):
        subreddits = [subreddits]
    backoff_429_received = False
    first_try = True
    limit = 100
    start_end = end
    start_beginning = beginning
    date_limit = end
    for term in terms:   
        beginning_timestamp = start_beginning
        end = add_time(beginning_timestamp,time_seg,segments)
        last_one = None
        full_data.update({term: []})
        data = []
        #print((datetime.datetime.fromtimestamp(beginning_timestamp)))
        #print((datetime.datetime.fromtimestamp(end)))
        print((datetime.datetime.fromtimestamp(date_limit)))
        #print(beginning_timestamp)
        #print(term+"\n")
        while (beginning_timestamp <date_limit) & (end<=date_limit):
            if last_one is None:
                beginning_timestamp = beginning
                end = add_time(beginning_timestamp,time_seg,segments)
            else:
                # this could skip posts if they were posted at the same exact time - down to milliseconds
                beginning_timestamp = add_time(last_one['created_utc'],time_seg,segments)
                end = add_time(beginning_timestamp,time_seg,segments)

            print("Querying pushshift. Beginning: [{0}]\tEnd: [{1}]".format(datetime.datetime.fromtimestamp(beginning_timestamp), datetime.datetime.fromtimestamp(end)))
            if backoff_429_received:
                print("429 response received from pushshift - waiting 2 minutes")
                time.sleep(60)
                backoff_429_received = False
            endpoint = f"https://apiv2.pushshift.io/reddit/comment/search/" \
                    f"?limit={limit}" \
                    f"?q={term}"\
                    f"&after={beginning_timestamp}" \
                    f"&before={end}" \
                    f"&fields=id,body,full_link,created_utc"\
                    f"&sort_type=created_utc&sort=asc"
            for sub in subreddits:
                endpoint = endpoint + "&subreddit={0}".format(sub)
            print(endpoint)
            response = requests.get(endpoint)
            if response.status_code == 429:
                backoff_429_received = True
            try:
                thisdata = response.json()['data']
                data.extend([thisdata])
                
                # this request was successful, reset first_try
                first_try = True
                if len(thisdata) > 0:
                    # go back for more data. find the last post in the returned data in order to set the 'after' parameter
                    last_one = thisdata[len(thisdata) - 1]
                else:
                    print("done querying for today. len data: {0}".format(len(data)))
                    break
            except (json.decoder.JSONDecodeError, simplejson.errors.JSONDecodeError) as e:
                if not first_try:
                    print("This is the second exception with this query, giving up and raising the exception")
                    raise Exception("{0} response from pushshift: {1}".format(response.status_code, e))
                print("Couldn't decode response -- {0}\nResponse: {1}.\nSleeping 1 minute".format(str(e), str(response)))
                time.sleep(30)
                print("Trying the same query again")
                first_try = False
        full_data[term]=data
            #pprint(data)
    return full_data

#get submission ids relating to term
#use praw to extract
#perform counting/sentiment analysis

#number of comments looked at displayed maybe???
def filterPushshiftData(data,datatype,terms):
    sorted_labels = []
    count = 0
    #cd =""
    chart_data ={}
    chard_data2 ={}

    for term in terms:
        countlst = []
        chart_data[term] = {
            'term':term,
            'data': [],
            'labels':sorted_labels
        } 
            
        for date_seg_lst in data[term]:
            count=0
            for i in range(len(date_seg_lst)):
                count += date_seg_lst[i]['body'].count(term)
                if isinstance(date_seg_lst[i]['created_utc'],int):
                    date_seg_lst[i]['created_utc'] = datetime.datetime.fromtimestamp(date_seg_lst[i]['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
                if i==0 and term==terms[0]:
                    sorted_labels.append(date_seg_lst[i]['created_utc'][:10])
            countlst.append(count)
            
        chart_data[term]['data']=countlst
        chart_data[term]['labels'] = sorted_labels
    pprint(chart_data)
    
    # cd = chart_data[terms[0]]
    # for i in range(len(terms)):

    #     cd = json.dumps(chart_data[term],indexnt =4)
    return chart_data

#multiple terms
#posts so limit is relevant

#sentiment analysis 

def get_graph_data(sub,terms,after,before,datetype,seg):
    preFilteredData = getPostsFromPushshift(sub,terms,after,before,datetype,seg)
    #print(preFilteredData)
    data =filterPushshiftData(preFilteredData,datetype,terms.split(","))
    #pprint(data)
    return data

# a = int(datetime.datetime(2022,1,5).timestamp())
# b = int(datetime.datetime(2022,1,10).timestamp())

# print(get_graph_data('childfree','breed,baby',a,b,'days',1))
