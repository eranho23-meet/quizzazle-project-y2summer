from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

#  (cmd prompt copy paste to get here)


config = {
  'apiKey': "AIzaSyD5JKVUF9g_sagdMdftpvk1qFSOABJkDoY",
  'authDomain': "quizzazle-meety2.firebaseapp.com",
  'projectId': "quizzazle-meety2",
  'storageBucket': "quizzazle-meety2.appspot.com",
  'messagingSenderId': "455984853974",
  'appId': "1:455984853974:web:e50d37c3b01ac4285eea77",
  'measurementId': "G-CG2FG52XDQ",
  "databaseURL": "https://quizzazle-meety2-default-rtdb.europe-west1.firebasedatabase.app"
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'





@app.route('/')
def home():
	is_logged = False
	if 'user' in login_session:
		is_logged = True
	return render_template('home.html', is_logged=is_logged)










if __name__ == '__main__':
    app.run(debug=True)