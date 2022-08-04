from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import random



# cd Documents/GitHub/quizzazle-project/quizzazle
# (cmd prompt copy paste to get here)



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
def home(): # home page, nothing special just to go from place to place
	is_logged = False
	if 'user' in login_session:
		if login_session['user']:
			is_logged = True	
	return render_template('home.html', is_logged=is_logged)



@app.route('/slogin', methods=['GET', 'POST']) 
def slog_in():
	if request.method == 'POST':
		mail = request.form['email']
		word = request.form['password']

		try:
			username = request.form['username']
			# if username == '':
			# 	raise('Exception')
			user = {'mail':mail, 'password':word, 'username':username, 'correct':0, 'wrong':0}
			login_session['user'] = auth.create_user_with_email_and_password(mail, word)
			db.child('Users').child(login_session['user']['localId']).set(user)
		except:
			try:
				login_session['user'] = auth.sign_in_with_email_and_password(mail, word)
				return redirect(url_for('add_tweet'))
			except:
				print('ERRORROROROROROROR bad')
		return redirect(url_for('home'))

	logging_in = True
	if 'user' in login_session: # checks if there is a user connected or was connected
			logging_in = False

	return render_template('slog_in.html', logger=logging_in)



@app.route('/logout')
def log_out():
	if 'user' in login_session:
		login_session['user'] = None
		auth.current_user = None
	return redirect(url_for('home'))



@app.route('/add_question', methods=['GET', 'POST']) 
def add_question():
	if request.method == 'POST':
		question = request.form["question"]
		awnser_1 = request.form["awnser1"]
		awnser_2 = request.form["awnser2"]
		awnser_3 = request.form["awnser3"]
		awnser_4 = request.form["awnser4"]

		me = login_session['user']['localId']
		my_info = dict(db.child("Users").child(me).get().val())
		my_name = my_info['username']

		question_dict = {
			'question': question,
			'by': me,
			'username': my_name,
			'answers': {
					awnser_1: True,
					awnser_2: False,
					awnser_3: False,
					awnser_4: False }	}

		db.child('questions').push(question_dict)
	
	return render_template('add_question.html')



@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
	if request.method == 'POST':
		if request.args.get('f') == 'f1':
			if 'user' in login_session:
				if not login_session['user'] == None:
					me = login_session['user']['localId']
					rightness = dict(db.child("Users").child(me).get().val())['correct'] + 1
					db.child("Users").child(me).update({'correct':rightness})
			return redirect(url_for('answer_correct'))

		elif request.args.get('f') == 'f2':
			if 'user' in login_session:
				if not login_session['user'] == None:
					me = login_session['user']['localId']
					wrongness = dict(db.child("Users").child(me).get().val())['wrong'] + 1
					db.child("Users").child(me).update({'wrong':wrongness})
			return redirect(url_for('answer_wrong'))

	else:
		all_questions_id = list(db.child('questions').get().val().keys())
		random_id = random.choice(all_questions_id)
		random_question = list(db.child('questions').child(random_id).get().val().values())
		answers = random_question[0]
		question = random_question[2]

		return render_template('quiz_yourself.html', answers=list(answers.keys()), correct=list(answers.values()), question=question)



@app.route('/my_stats')
def stats():
	try:
		me = login_session['user']['localId']
		rightness = dict(db.child("Users").child(me).get().val())['correct']
		wrongness = dict(db.child("Users").child(me).get().val())['wrong']
		return render_template('user_stats.html', right=rightness, wrong=wrongness)
	except:
		return redirect(url_for('home'))



@app.route('/quiz/correct')
def answer_correct():
	return render_template('is_correctC.html')



@app.route('/quiz/wrong')
def answer_wrong():
	return render_template('is_correctW.html')



if __name__ == '__main__':
    app.run(debug=True)
