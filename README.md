#### A Data pipeline to fetch the mood score, activities and sleep of all the users who have been active on a certain day to analyse user’s check in for mood (mood score) and their level of activity based on steps/active minutes, sleep
## Prerequisites: 
* Python 
* Mongodb
* pymongo
## How to run
* First run `insert_collection.py` file to create a database by name wysa and also to create 4 collections namely `{'User', 'Mood', 'Activity','Sleep'}`
* Then run `aggregate.py` file which will create an aggregate pipeline and will also dump the results into `results.json` file
