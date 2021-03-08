
# OnSight: Outdoor Rock Climbing Recommendations

Recommendations for outdoor rock climbing has historically been limited to word of mouth, guide books, and most popular climbs. With our project OnSight, we believe we can offer personalized recommendations for outdoor rock climbers.

Disclainer: With rock climbing, especially outdoors, there is an inherent risk that is taken when you decide to climb. Although our recommender tries to offer routes similar to the ones users have done, there is still a risk that the route may be too hard and therefore dangerous. This is not a problem that is solely put on the recommender, but a problem with rock climbing as a whole. There is no standard in climbing grades, but rather it is an agreement among the climbers that have climbed that route. Therefore climbing grades are subjective, and climbs may be harder and more dangerous than a user expects. We realize this, and we encourage everyone to look at the safety information of each climb on its corresponding climbing page on Mountain Project.

## How To Run

* To just use the project, visit https://dsc180b-rc-rec.herokuapp.com/. Note that this project runs on a free dyno, so when traffic to the site is low, response times will be very slow. Be patient!
* To run on the command line, clone the repository, then run the command "pip install -r requirements.txt" from the project home.

### Running the Project on the Command Line

To run the project, every command must start with "python run.py" from the root directory of the project. By default, "python run.py" will not download data, will use the default data/model parameters, will not use cuda, will not run any benchmarks, and will train and evaluate SASRec on the Beauty dataset. The base command can be modified with a couple of different flags:

|Flag|Type|Default Value|Description|
|-|-|-|-|
|-d, --data|bool|False|Use this flag to run all data scraping code. This will take a very long time, upwards of 48 hours total to get all the data. It is recommended *not* to run this. Be warned that using this flag will first delete **ALL** raw and cleaned data, before downloading new raw data. |
|-c, --clean|bool|False|Use this flag to run all data cleaning code. Be warned that using this flag will first delete **ALL** raw and cleaned data, before processing raw data into cleaned data.|
|-p, --top-pop|bool|False|Use this flag to return the top 10 most popular/well received as a csv.|
|-\-data-config|str|"config/data_params.json"|The location at which data parameters can be found|
|-\-test|bool|False|Use this flag to run the data pipeline and top pop on a small sample. This will override all other flags|
|-\-delete|bool|False|Use this flag to wipe out all data from MongoDB|
|-\-upload|bool|False|Use this flag to upload cleaned data to MongoDB|

### Description of Parameters

#### Data Parameters

|Parameter Name|Type|Default Value|Description|
|-|-|-|-|
|raw_data_folder|str|data/raw/|The location at which raw data will be saved. Note that this path is relative to the project root.|
|clean_data_folder|str|data/cleaned/|The location at which clean data will be saved. Note that this path is relative to the project root.|

#### Model Parameters

|Parameter Name|Type|Default Value|Description|
|-|-|-|-|
|TODO|TODO|TODO|TODO|

There are none so far
