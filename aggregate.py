import pymongo 
import json

if __name__ == '__main__':
    #connecting to the local server
    client=pymongo.MongoClient("mongodb://localhost:27017")
    db = client['wysa']
    #creating collections
    user_collection = db['User']

    mood_collection = db['Mood']
    
    activity_collection = db['Activity']
    
    sleep_collection = db['Sleep']

   

    results=list(user_collection.aggregate([
        
        {    
        "$lookup": {

            "from": "Mood",
            "localField":"_id",
            "foreignField":"user",
            "as":"mood_score",
            
            "pipeline":[{
                "$project":{
                    "_id":0,
                    "mood_score":"$value"
                }
            }]
            }
        },
        {    
        "$lookup": {

            "from": "Activity",
            "localField":"_id",
            "foreignField":"user",
            "as":"activity"  ,

            "pipeline":[
                {
                "$match": {
                    "date":"04-05-2022"}
                },
                {
                "$group": {
                    "_id": "$activity",
                    "steps": { "$sum" : "$steps" },
                    "duration": {"$sum" : "$duration"},
                    "distance": {"$sum" : "$distance"}}
                },
                {"$project":{
                    "_id":0,
                    "activity":"$_id",
                    "steps":"$steps",
                    "distance":"$distance",
                    "duration":"$duration",
                }}
                
            ] 
        }

       },
       {    
        "$lookup": {

            "from": "Sleep",
            "localField":"_id",
            "foreignField":"user",
            "as":"sleep"  ,

            "pipeline":[
                {
                "$match": {
                    "date":"04-05-2022"},
                

                },
                {"$project":{
                    "_id":0,
                    "sleep":"$sleep score",
                    "hours_of_sleep":"$hours of sleep",
                    "Hours_in_bed":"$hours in bed"
                }}
            ] 
        }

       },
       {"$project":{
        "_id":0,
        "user":"$_id",
        "date":"$createdAt",
        "mood_score":{"$arrayElemAt":["$mood_score.mood_score",0]},
        "activity": "$activity",
        "sleep":"$sleep"
       }
       }
       
        
    ]))
with open("results.json", 'w') as fp:
    json.dump(results, fp, indent=4, default=str)  
