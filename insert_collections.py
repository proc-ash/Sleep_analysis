import pymongo 
from datetime import datetime
import pandas as pd
if __name__ == '__main__':
    #connecting to the local server
    client=pymongo.MongoClient("mongodb://localhost:27017")
    print('done')
    #creating database 
    db = client['wysa']
    #creating collections
    collection=db['User']
    
    insert_users=[
    {"_id": "A", "name": "brad", "timezone": "Americas/Los Angeles", "version": 70, 
        "app": "Wysa", "country": "US", "createdAt": datetime.strptime("2021-04-05T15:56:11.553Z", "%Y-%m-%dT%H:%M:%S.%fZ"), "updatedAt": datetime.strptime("2021-04-05T15:56:46.392Z", "%Y-%m-%dT%H:%M:%S.%fZ")},
        {"_id": "B", "name": "Tim", "timezone": "Americas/Calafornia", "version": 60, 
        "app": "Wysa", "country": "US", "createdAt": datetime.strptime("2021-04-03T15:56:11.553Z", "%Y-%m-%dT%H:%M:%S.%fZ"), "updatedAt": datetime.strptime("2021-04-03T15:56:46.392Z", "%Y-%m-%dT%H:%M:%S.%fZ")}
    ]

    collection.insert_many(insert_users)

    collection=db['Mood']
    insert_mood=[
        {"_id" : "M_A", "field" : "mood_score", "user" : "A", "value" : 8, # mood_score is stored as a scale of 1-10
            "createdAt": datetime.strptime("2021-04-05T15:56:11.553Z", "%Y-%m-%dT%H:%M:%S.%fZ"), "updatedAt": datetime.strptime("2021-04-05T15:56:46.392Z", "%Y-%m-%dT%H:%M:%S.%fZ")},
        
        {"_id" : "M_B", "field" : "mood_score", "user" : "B", "value" : 6, # mood_score is stored as a scale of 1-10
            "createdAt": datetime.strptime("2021-04-03T15:56:11.553Z", "%Y-%m-%dT%H:%M:%S.%fZ"), "updatedAt": datetime.strptime("2021-04-03T15:56:46.392Z", "%Y-%m-%dT%H:%M:%S.%fZ")}

    ]
    collection.insert_many(insert_mood)
    
    activity_df = pd.read_csv('activity_data_csv.csv')

    activity_col = ['user','date','start time','end time', 'duration', 'activity', 'log type', 'steps', 'distance', 'elevation gain', 'calories']

    sleep_df = pd.read_csv('sleep_data_csv.csv')

    sleep_col = ['user', 'day', 'date' ,'start time', 'sleep score', 'hours of sleep', 'hours in bed']

    collection=db['Activity']

    activity_res = []

    for idx, row in activity_df.iterrows():
        row_values = row.to_dict()
        new_entry = {}
        for col_name in activity_col:
            new_entry[col_name] = row_values[col_name]
        activity_res.append(new_entry)

    collection.insert_many(activity_res)

    collection=db['Sleep']

    sleep_res = []

    for idx, row in sleep_df.iterrows():
        row_values = row.to_dict()
        new_entry = {}
        for col_name in sleep_col:
            new_entry[col_name] = row_values[col_name]
        sleep_res.append(new_entry)
    
    collection.insert_many(sleep_res)












