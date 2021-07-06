# todokar.com
This todo task manager lets you manage and analyse your to-do tasks and day to day habits more interactively. It also gets you motivated to stick to your habit by gaining points according to your dedication. 
Check out further for more details of running the flask server on your own setup.

## System Requirements
The server can run on any platform given it has python and mongodb installed in it.
Required version of python: >=3.7
To install the dependencies, make sure you have pipenv install in your python packages. To install it, run the command `pip install pipenv`.
To install mongodb, please follow the steps corresponding to your system.

##Installing and Running the Flask Server
1. Clone the repository into you local machine using `git clone` command.
2. Create the virtual env using the command `pipenv install` and enter it using `pipenv shell`.
3. To run the flask server, run the command `flask run`. By default the server wil run on localhost and 5000 port id. You can pass the custom arguments to change this default setting.
4. Make sure the mongodb server is up and running in the location specified in the `config.py` file. This is for the flask server to contact DB and perform tasks and user operations.
5. You can reach to the home page of todokar.com website by using the url `127.0.0.1:5000/`.
