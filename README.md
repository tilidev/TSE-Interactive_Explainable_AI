# Team Project Software Development - Development of an interactive explainable AI application

---

**Authors**: Felix Hasse, Nicolas Kiefer, Isabelle Konrad, Tilio Schulze
**Version**: 1.0

[[_TOC_]]

## First Steps

### Environment and dependencies

### Run application

Terminal 1:
```shell
cd API/
python main.py
```

Terminal 2:
```shell
cd Frontend/app/
npm run serve
```

The API interactive docs are accessible with http://localhost:8000/docs.
The root for all API requests is http://localhost:8000/. \
The application gui is accessible with http://localhost:8080/.
The starting page is "/dataset". To access the admin panel, use "/admin".

## Project structure

The application consists of a desktop front-end gui and a backend api server. The front-end is built with the [VUE](https://vuejs.org)-Javascript framework, the back-end api with the [FastAPI](https://fastapi.tiangolo.com)-python framework.

![project structure](/uploads/47aa8caab144de1185aaf9e9fa3f06b5/image.png)

## Back-End

### Overview of Files

The Back-end files can be found in the folder "API/". Here is a short summary about what each file or directory does:

`main.py`:
- starting point for FastAPI process
- defines the API requests accessible by the front-end
- contains documentation for interactive FastAPI docs (http://localhost:8000/docs)
- launches explanation sub-processes defined in `task_gen.py`
- defines manager process for shared process memory

`models.py`:
- defines the [pydantic](https://pydantic-docs.helpmanual.io) models for requests, responses and other data schemas
- using models ensures data validation and basic type conversion

`constants.py`:
- defines commonly used strings and numbers to reduce magic strings
- contains the constraints for the dataset attributes
- defines dictionary mappings for data transformations 

`database_req.py`:
- interface for database interaction with the API
- defines functions for database access, seperates database logic and structure from API requests

`task_gen.py`:
- defines explanation sub-process logic for lime and shap
- access to shared memory (job queue, explanation results dictionary)
- defines timeout logic for explanation results

`lime_utils.py`:


`shap_utils.py`:


`preproc.pickle`:


`DataLoader_ey.py`:
- taken from the xai reference project and slightly adapted
- method data_loader to load the credit data, drop the unused columns and remove outliers
- preprocessing method for preparing data for model prediction
- method for adding AI recommendation and confidence


`database.db`:
- SQLite database for application, counterfactual information and experimentation information storage
- overview over structure and methods provided below


`smote_ey.tf/`:
- the trained tensorflow model from the xai reference project 
- used for AI recommendation and confidence and explanation generation


`Data/`:
- folder containing the raw data that was read into the database
- contains the german credit dataset in csv format and 
- contains the counterfactuals in json format, the `all_counterfactuals.json` contains the initially generated counterfactuals, the `cfs_response_format.json` a reformatted version of the counterfactuals that was added to the database



### SQLite Database

The application uses a SQLite database for saving the cleaned german credit dataset ([GCD](https://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29)), the experiments and the corresponding results, aswell as pre-generated `DICE` counterfactuals for each loan application. The python module [SQLite3](https://docs.python.org/3.8/library/sqlite3.html) is used as the database interface for the API.
\
An overview of the different tables and their strucutre is provided below. Below that, you can find an overview of the relevant database interaction functions. These are defined in the file `database_req.py` which is located in the "API/" folder
___

**Database Table Structure:**
![Database Table Structure](/uploads/4ad0c44ad40601306c83409a1cda3c51/image.png) 
All cleaned applications from the GCD are stored in the applicants table. The attributes foreign_worker, status_sex_ and classification_ were dropped and NN_recommendation and NN_confidence added. These two attributes refer to the actual model prediction for this application and were determined using the `smote_ey.tf` model.\
The dice table contains the pregenerated counterfactuals for the applications of the GCD. The counterfactuals column contains this information in json format. These jsons have the key 'counterfactuals' referring to a list of 5 counterfactuals in json format. This is necessary because SQLite cannot store lists.\
The elements in the dice table have the primary key instance_id, which refers to the ids in the applicants table. Therefore when an element in the applicants table is deleted or changes its id, the according element in the dice table should be deleted or changed as well.\
The experimentation functionality is covered by the databases experiments and results. In the experiments table all the relevant information for the defined experiments, like the type of explanation and ids of applications that should be shown are stored in json format. The json contains the keys, which are defined for the ExperimentInformation model in the `models.py` file. The results table is used to store the decisions of a user for a certain experiment. They are stored in json format. The json contains jsons in the SingleResult format defined in the `models.py` folder. Their loan id is the key to reference those SingleResult jsons.\
The key experiment_name of the results table references the attribute name in the experiments table. Therefore when an experiment is deleted or changes its name, this change should also apply to the results table.

___

**Database Interaction:**
![Database Interaction](/uploads/b58c7e493f24e5a1926cde76ecc5e64a/image.png)

___

Explanation Task flow: `rgb(133, 192, 255)`\
Explanation Result flow: `rgb(217, 155, 255)`
![Explanations compuation & data flow](/uploads/164a51e39b282a5dcd504bbb3997e6d4/Api_Explainer_Flow.jpg)

## Front-End

