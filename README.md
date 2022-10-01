# project-03
Python Flask API Project (Project 3)
Malta08 (Fake Company) Employee Directory App

---------
## Part 1

### Libraries and Modules
- This application uses Flask and SQLite3 libraries.
- SQLite3 is a standard Python library.
- To install Flask:
    - pip install flask

All CSS files can be found in the `static` directory and all HTML files can be found in the `templates` directory.

### Major End Points
- /          -> Home Page
- /home      -> Home Page
- /login     -> User Log In Page
- /logout    -> User Log Out (removes user from the session)
- /directory -> Employee Directory (list) Page
- /employees -> Returns all employee data in the database in JSON

There is more (such as "/add", "/delete", etc.) endpoints. Please refer to alta3research-flask01.py for more information.

---------
## Part 2

### Libraries and Modules
- This program uses csv, yaml, and requests libraries.
- csv is a standard library.
- To install requests:
    - pip install requests
- To install yaml:
    - pip install pyyaml
- To install pandas:
    - pip install pandas

### Parse JSON as more human-friendly formats
JSON returned from the Flask App API is parsed and processed as the following:
- Printed to the terminal as yaml (using pprint)
- Saved as a .csv file
