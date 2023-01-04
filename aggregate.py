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

    var_date=input("Enter start date e.g. (mm-dd-yyyy): ")
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
                "$match": {'date':{"$gte":var_date}}
                },
                {
                "$group": {
                    "_id": {"activity":"$activity","date":"$date"},
                    "steps": { "$sum" : "$steps" },
                    "duration": {"$sum" : "$duration"},
                    "distance": {"$sum" : "$distance"}}
                },
                
                {"$project":{
                    "_id":0,
                    "activity":"$_id.activity",
                    "activity_date":"$_id.date",
                    "steps":"$steps",
                    "distance":"$distance",
                    "duration":"$duration",
                }},
                {
                    "$sort":{"activity_date":1}
                }
                
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
                "$match": {'date':{"$gte":var_date}},
                

                },
                
                {"$project":{
                    "_id":0,
                    "sleep_date":"$date",
                    "sleep":"$sleep score",
                    "hours_of_sleep":"$hours of sleep",
                    "Hours_in_bed":"$hours in bed"
                }},
                {
                    "$sort":{"sleep_date":1}
                }
            ] 
        }

       },
       {"$project":{
        "_id":0,
        "user":"$_id",
        "mood_score":{"$arrayElemAt":["$mood_score.mood_score",0]},
        "activity": "$activity",
        "sleep":"$sleep"
       }
       }
       
        
    ]))
with open("results.json", 'w') as fp:
    json.dump(results, fp, indent=4, default=str)  
