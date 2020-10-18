import pyrebase
import os

config = {
    "apiKey": os.environ['API_KEY_FIREBASE'],
    "authDomain": "whats-on-my-fridge.firebaseapp.com",
    "databaseURL": "https://whats-on-my-fridge.firebaseio.com",
    "projectId": "whats-on-my-fridge",
    "storageBucket": "whats-on-my-fridge.appspot.com",
    "messagingSenderId": "859429652765",
    "appId": "1:859429652765:web:06a4299a668473acbb79f4"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

email = 'test@gmail.com'

password = '1234567890'

user = auth.sign_in_with_email_and_password(email,password)
print(user)

data = {'name': 'Me!'}
results =db.child("users").get()

class User:
    def __init__(self, email, password, login=False, register=False):
        """
        docstring
        """
        self.email = email
        self.password = password
        
        # Log in
        response = auth.sign_in_with_email_and_password(self.email, self.password)
        self.id_token = response['IdToken']
        self.local_id = response['localId']
        self.registered = bool(response['registered'])
        self.refresh_token = response['refreshToken']
        self.expires_in = response['expiresIn']
    
    def refresh(self):
        response = auth.refresh(self.refresh_token)
        self.id_token = response['IdToken']
        self.local_id = response['localId']
        self.registered = bool(response['registered'])
        self.refresh_token = response['refreshToken']
        self.expires_in = response['expiresIn']

class FireDataBase():
    def __init__(self):
        """
        docstring
        """
        self.db = firebase.database()
