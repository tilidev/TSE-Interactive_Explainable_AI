# Team Project Software Development - NAME

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

## Project structure

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


`database.db`:


`smote_ey.tf/`:


`Data/`:



### SQLite Database

The application uses a SQLite database for saving the cleaned german credit dataset ([GCD](https://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29)), the experiments and the corresponding results, aswell as pre-generated `DICE` counterfactuals for each loan application. The python module [SQLite3](https://docs.python.org/3.8/library/sqlite3.html) is used as the database interface for the API.
\
An overview of the different tables and their strucutre is provided below. Below that, you can find an overview of the relevant database interaction functions. These are defined in the file `database_req.py` which is located in the "API/" folder
___

**Database Table Structure:**
![Database Table Structure](/uploads/4ad0c44ad40601306c83409a1cda3c51/image.png)
___

**Database Interaction:**
![Database Interaction](/uploads/b58c7e493f24e5a1926cde76ecc5e64a/image.png)

Explanation Task flow: `rgb(133, 192, 255)`\
Explanation Result flow: `rgb(217, 155, 255)`
![Explanations compuation & data flow](/uploads/164a51e39b282a5dcd504bbb3997e6d4/Api_Explainer_Flow.jpg)

## Front-End

