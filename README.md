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

### SQLite Database

The application uses a SQLite database for saving the cleaned german credit dataset ([GCD](https://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29)), the experiments and the corresponding results, aswell as pre-generated `DICE` counterfactuals for each loan application. The python module [SQLite3](https://docs.python.org/3.8/library/sqlite3.html) is used as the database interface for the API.
\
An overview of the different tables and their strucutre is provided below. Below that, you can find an overview of the relevant database interaction functions. These are defined in the file `database_req.py` which is located in the "API/" folder
___

**Database Table Structure:**
![Database Table Structure](/uploads/4ad0c44ad40601306c83409a1cda3c51/image.png)
___

**Database Interaction:**
![Database Interaction](/uploads/99f6e1cf809f3b982885bb8aa803fe5a/image.png)

Explanation Task flow: `rgb(133, 192, 255)`\
Explanation Result flow: `rgb(217, 155, 255)`
![Explanations compuation & data flow](/uploads/164a51e39b282a5dcd504bbb3997e6d4/Api_Explainer_Flow.jpg)

## Front-End

