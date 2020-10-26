# What's on my Fridge

Code for the competition from it-talents.de ([October 2020](https://www.it-talents.de/foerderung/code-competition/code-competition-10-2020-edeka-digital))

## Set Up

The following steps will guide you through setting up all the necessary dependencies to test the code.

### Python and Dependencies

to use the code you will need a python installation, i would strongly recomend using [Python 3.7.9](https://www.python.org/downloads/release/python-379/).

1. Install python on your system and create a new virtual enviroment using Python virtualenv

```bash
python -m virtualenv whatsonmyfridge_venv
```

2. Activate the Enviroment
```bash
whatsonmyfridge_venv\Scripts\activate
```
if you're in a bash terminal, instead do:
```bash
source whatsonmyfridge_venv/Scripts/activate
```
Your terminal should now preface the path with something like ```(whatsonmyfridge_venv)```, indicating that the whatsonmyfridge_venv environment is active. 

3. Install the necessary dependecies

Using the file ```requirements.txt``` in the repository, install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Make a fix on the Kivy installation

sadly the actual version of kivy has a little bug that will not allow us to load the images correctly, to fix this open the ```loader.py``` in the virtual enviroment

```
whatsonmyfridge_venv\Lib\site-packages\kivy\loader.py
```
and change the following block (aprox line 334):
```python
#...
if (
    Config.has_section('network')
    and 'useragent' in Config.items('network')
):
#...
```
to:
```python
#...
if Config.has_option('network', 'useragent'):
#...
```

this should solve the problem.

### Recipe API

if you are accessing this from the competition Application you can use the APIKey that i provided with the project, if not you need to get your own API key from [Spoonacular](https://spoonacular.com/food-api/console#Profile)

after getting your Spoonacular APIKey, you will need to set an enviroment variable

```bash
export API_KEY_SPOONACULAR="1234YOURAPIKEY890"
```

Now our are all set!

## Running the Script

make sure that the enviroment is acivated (Your terminal should now preface the path with something like ```(whatsonmyfridge_venv)```). and make sure that the ```API_KEY_SPOONACULAR``` is set up (you can use ```echo $API_KEY_SPOONACULAR``` in linux or ```echo %API_KEY_SPOONACULAR%``` in Windows).

then run the main.py file using python

```bash
python main.py
```

