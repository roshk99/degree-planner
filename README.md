# Degree Planner
An online platform that allows students to plan their entire college schedule
Copyright 2015

### Running the application
* Install Python Version 2.7 or higher (https://www.python.org/downloads/)
* Install Google App Engine for Python (https://cloud.google.com/appengine/downloads)
    + Make sure you add product path to your PATH
    + In Windows, there is a checkbox in the installer
    + In Linux/Mac, it should be the following command with the path being the path to the google_appengine folder created: `PATH=$PATH:/home/computer_name/Desktop/google_appengine/`
* Clone the repository
    + This will create a degree-planner folder
* Run the App Engine in Windows
    + Double-click the application. Go to `File`, `Add Existing Application`
    + Navigate to the degree-planner folder for the Application Path
    + The admin port will be 8000
    + The port will be 8080
    + The name should say 'degree-planner'
    + Click the Run button in the top-left corner. Wait until the browse button is activated, and then click it
    + The project should open in your browser at http://localhost:8080
    + To stop running the application, just press the Stop button
* Run the App Engine in Mac/Linux
    + In the command line, navigate to the directory just above degree-planner
    + Type the following command: `dev_appserver.py degree-planner`
    + The project will be running at http://localhost:8080
    + To stop running the application, just enter `[Ctrl] + c`

### Server Logs and Database
* To view the server logs
    + In Windows, just click the Logs button in Google App Engine
    + In Mac/Linux, the logs will just appear in the command prompt window
* To view the local database, navigate to http://localhost:8000/datastore in the browser



