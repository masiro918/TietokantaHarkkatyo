from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/profiles/<string:username>")
def profiles(username):
	
	
	user_id = get_by_username(username)
	
	sql = "SELECT * FROM users WHERE id=:user_id;"
	result = db.session.execute(sql, {"user_id":user_id})
	results = result.fetchone()
	
	username = results[1]
	role = results[2]
	age = str(results[3])
	about_me = str(results[4])
	
	
	return render_template("profile.html", username=username, age=age, about_me=about_me, role=role)
	
@app.route("/edit_profile")
def edit_profile():
	user_id = get_user_id()
	
	sql = "SELECT * FROM users WHERE id=:user_id;"
	result = db.session.execute(sql, {"user_id":user_id})
	results = result.fetchone()
	
	
	
	username = results[1]
	age = str(results[3])
	about_me = str(results[4])
	
	return render_template("edit_profile.html", username=username, age=age, about_me=about_me)
	
@app.route("/new_moderator")
def new_moderator():
	sql = "SELECT * FROM users ORDER BY username;"
	result = db.session.execute(sql)
	users = result.fetchall()
	return render_template("new_moderator.html", users=users)
	
@app.route("/make_moderator/<int:user_id>")
def make_moderator(user_id):
	user = get_username()
	
	if (user == "admin"):
		username = get_by_user_id(user_id)
		
		sql = "UPDATE users SET role='moderator' WHERE id=:user_id;"
		db.session.execute(sql, {"user_id":user_id})
		db.session.commit()
		return render_template("new_mod_added.html")
	else:
		return "Sinulle ei ole lupaa tähän toimenpiteeseen!"
	return "Sinulle ei ole lupaa tähän toimenpiteeseen!"
	
@app.route("/delete_messages")
def delete_messages():
	return render_template("delete_messages.html")
	
@app.route("/delete_message", methods=["POST"])
def delete_message():
	topic_id = request.form["topic_id"]
	message_id = request.form["message_id"]
	
	
	
	# now we check, if user is admin-user or moderator
	username = get_username()
	
	if (is_moderator(username) == True):
		sql = "DELETE FROM messages WHERE id=:message_id;"
		db.session.execute(sql, {"message_id":message_id})
		db.session.commit()
		return redirect("/topic?topic_id=" + topic_id)
		
	if (username == "admin"):
		return redirect("/topic?topic_id=" + topic_id)
	
	return ("Sinulla ei ole oikeuksia poistaa tätä viestiä!")
	


	
@app.route("/update_profile", methods=["POST"])
def update_profile():
	age = request.form["age"]
	about_me = request.form["about_me"]
	
	
	
	
	user_id = get_user_id()
	sql = "UPDATE users SET age=:age, about_me=:about_me WHERE id=:user_id;"
	db.session.execute(sql, {"age":age, "about_me":about_me, "user_id":user_id})
	db.session.commit()
	
	return redirect("/updates_done")
	
@app.route("/updates_done")
def updates_done():
	return render_template("updates_done.html")

    
@app.route("/new_topic")
def new_topic():
	return render_template("/new_topic.html")

@app.route("/add_topic", methods=["POST"])
def add_topic():
	title = request.form["title"]
	first_message = request.form["first_message"]
	
	user_id = get_user_id();
	
	sql = "INSERT INTO topics (title, timestamp, question_content, user_id) VALUES (:title, NOW(), :first_message, :user_id);"
	db.session.execute(sql, {"title":title, "first_message":first_message, "user_id":user_id})
	db.session.commit()
	
	return render_template("topic_added.html")
    
@app.route("/topics")
def topics():
	msg_count = int(request.args["msg_count"])
	
	result = db.session.execute("SELECT * FROM topics ORDER BY \"timestamp\" DESC;")
	topics = result.fetchall()	

	
	aiheita = len(topics)
	topic_list = []
	
	if (msg_count > aiheita):
		for i in range(aiheita):
			topic_id = topics[i][0]
			user_id = topics[i][4]
			username = get_by_user_id(user_id)
			timestamp = topics[i][2]
			question_content = topics[i][3]
			title = topics[i][1]
			topic_list.append(Topics_view(topic_id, title, timestamp, question_content, username))
	else:
		for i in range(msg_count):
			topic_id = topics[i][0]
			user_id = topics[i][4]
			username = get_by_user_id(user_id)
			timestamp = topics[i][2]
			question_content = topics[i][3]
			title = topics[i][1]
			topic_list.append(Topics_view(topic_id, title, timestamp, question_content, username))
		
	
	return render_template("topics.html", topics=topic_list)

@app.route("/previous_page")
def previous_page():
	down_value = int(request.args["previous"])
	top_value = int(request.args["next"])
	
	down_value = down_value - 4;
	top_value = top_value - 4;
	return redirect("/topics?down_value=" + str(down_value) + "&top_value=" + str(top_value))
	
@app.route("/next_page")
def next_page():
	down_value = int(request.args["previous"])
	top_value = int(request.args["next"])
	
	down_value = down_value + 4;
	top_value = top_value + 4;
	return redirect("/topics?down_value=" + str(down_value) + "&top_value=" + str(top_value))
	
	
@app.route("/topic")
def topic():
	topic_id = request.args["topic_id"]
	
	sql = "SELECT * FROM topics WHERE id=:topic_id;"
	result = db.session.execute(sql, {"topic_id":topic_id})
	topic_name = result.fetchone() 
	
	
	
	user_id = topic_name[4]
	questioner = get_by_user_id(user_id)
	
	
	
	sql_messages = "SELECT * FROM messages WHERE topic_id=:topic_id ORDER BY timestamp;"
	result_messages = db.session.execute(sql_messages, {"topic_id":topic_id})
	
	messages = result_messages.fetchall()
	
	
	
	if (messages == None):
		return render_template("topic.html", topic=topic_name[1], topic_id=topic_id, topic_timestamp=topic_name[2], question_content=topic_name[3], questioner=questioner)
	
	messages_list = []
	
	for i in range(len(messages)):
		content = str(messages[i][3])
		timestamp = str(messages[i][4])
		likes = str(messages[i][5])
		
		
		# now we search a sender of a message
		sql = "SELECT username FROM users WHERE id=:user_id;"
		result = db.session.execute(sql, {"user_id":messages[i][2]})
		results = result.fetchone()
		
		messages_list.append(Message_view(messages[i][0], messages[i][1], results[0], content, timestamp, likes))
		
		
		
		

	
	
	
	
	return render_template("topic.html", topic=topic_name[1], topic_id=topic_id, topic_timestamp=topic_name[2], question_content=topic_name[3], messages=messages_list, questioner=questioner)

@app.route("/new_message", methods=["POST"])
def new_message():
	topic_id = request.form["topic_id"]
	message_content = request.form["content"]
	
	user_id = get_user_id()
	
	
	
	
	sql = "INSERT INTO messages (topic_id, user_id, content, timestamp, likes) values (:topic_id, :user_id, :content, NOW(), 0);"
	db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id, "content":message_content,})
	db.session.commit()
	
	return redirect("/topic?topic_id=" + topic_id)
	
@app.route("/add_like")
def add_like():
	message_id = request.args["message_id"]
	topic_id = request.args["topic_id"]
	
	
	# now we get the count of likes
	sql_likes = "SELECT likes FROM messages WHERE id=:message_id;"
	result_messages = db.session.execute(sql_likes, {"message_id":message_id})
	likes_count = result_messages.fetchone()
	
	
	
	
	user_id = get_user_id()
	
	
	sql_liked = "SELECT COUNT(*) FROM likes WHERE user_id=:user_id AND message_id=:message_id;"
	liked_result = db.session.execute(sql_liked, {"user_id":user_id, "message_id":message_id})
	count = liked_result.fetchone()[0]
	
	
	
	if count == 0:
		# we add a new like
		sql_updated_likes = "INSERT INTO likes (user_id, message_id) VALUES (:user_id, :message_id);"
		db.session.execute(sql_updated_likes, {"user_id":user_id, "message_id":message_id})
		db.session.commit()
	else:
		# liking is forbidden
		return redirect("/topic?topic_id=" + topic_id)
	
	
	
	# now we add a new like
	updated_likes = likes_count[0] + 1
	
	
	
	sql_updated_likes = "UPDATE messages SET likes=:updated_likes WHERE id=:message_id;"
	db.session.execute(sql_updated_likes, {"updated_likes":updated_likes, "message_id":message_id})
	db.session.commit()
	
	return redirect("/topic?topic_id=" + topic_id)
	


@app.route("/register")
def register():
	return render_template("register.html")
	
@app.route("/logout")
def logout():
	destroy_session()
	return render_template("logout.html")
	
@app.route("/new_user", methods=["POST"])
def new_user():
	username = request.form["username"]
	password = request.form["password"]
	password2 = request.form["password2"]
	
	
	# we have to check if passwords are the same
	if not password == password2:
		return render_template("error_register.html", error_message_register="salasanat eivät täsmää")
	
	
	# now we check that this username does not exist
	if not user_exists(username):
		return render_template("error_register.html", error_message_register="käyttäjätunnus on jo olemassa! Valitse toinen nimi käyttäjätunnukselle.")
	
	
	
	# a password requires 6 or more characters. At least one number and four letters must be included
	password_ok = check_password(password)
	
	if password_ok == True:
		# now we make a password hash 
		password_hash = generate_password_hash(password)
		
		role = "registered_user"
		
		
		
		# now we add a new user to the database
		sql = "INSERT INTO users (username,role,password_hash) VALUES (:username,:role,:password_hash);"
		db.session.execute(sql, {"username":username, "role":role,"password_hash":password_hash})
		db.session.commit()
		
		return render_template("confirm.html")
	else:
		return render_template("error_register.html", error_message_register="salasana ei ole sallittu. Tiesithän, että salasanassa on oltava vähintään 6 merkkiä, joista vähintään 4:n täytyy olla kirjain ja 1:n numero")
		
		
@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	
	
	
	sql = "SELECT password_hash FROM users WHERE username =:username;"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()  
	
	hash_value = user[0]
	
	
	
	
	
	
	
	# if username or password is incorrect
	if user == None:
		return "väärät tunnukset"
	
	if check_password_hash(hash_value,password):
		# now we get a user type
		sql = "SELECT role FROM users WHERE username=:username;"
		result = db.session.execute(sql, {"username":username})
		results = result.fetchone() 
		user_type = results[0]
		
		create_session(username, user_type)
		
		return redirect("/")
	else:
		return "väärät tunnukset (salasana)"

	
	
	


@app.route("/confirm")
def confirm():
	return render_template("confirm.html")

@app.route("/error_register")
def error_register():
	return render_template("error_register.html")
	
@app.route("/control_panel")
def control_panel():
	return render_template("control_panel.html")
	
@app.route("/edit_users")
def edit_users():
	sql_moderators = "SELECT * FROM users WHERE role = 'moderator';"
	result = db.session.execute(sql_moderators);
	results_moderators = result.fetchall()
	
	sql_basic_users = "SELECT * FROM users WHERE role = 'registered_user';"
	result = db.session.execute(sql_basic_users);
	results_basic_users = result.fetchall()
	
	return render_template("/edit_users.html", moderators=results_moderators, basic_users=results_basic_users)
	

	
	

# the other functions 


# this function checks that a password is valid
def check_password(password):
	# a password must include at least 6 characters
	if (len(password) < 6):
		return False
	
	
	# also the password must includes at least 4 letters
	chars = 0
	
	for i in range(len(password)):
		char = password[i]
		
		
		# if ascii-code is < 65, the character is not a letter
		if (ord(char) > 65):
			chars = chars + 1
			
	
	if (chars < 4):
		return False
		
	numbers = 0
		
	
	# also there would be at least 1 number in password
	for i in range(len(password)):
		char = password[i]
		
		
		# if ascii-code is < 65, the character is not a letter
		if (ord(char) < 65):
			numbers = numbers + 1
			
	
	if (numbers < 1):
		return False
		
		
	return True



# checks if username is already in use
def user_exists(username):
	sql = "SELECT * FROM users WHERE username =:username;"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	
	if user == None:
		return True
	else:
		return False


# now we create session
def create_session(username, user_type):
	# we create a cookie that includes username and user type
	session["username"] = username
	session["usertype"] = user_type


# returns username of the session
def get_username():
	return session["username"]
	

# deletes coockie that includes username and type of username
def destroy_session():
	del session["username"]
	del session["usertype"]
	

# returns user-id
def get_user_id():
	user = get_username()
	
	sql = "SELECT * FROM users WHERE username=:user"
	result = db.session.execute(sql, {"user":user})
	results = result.fetchone() 
	
	user_id = results[0]
	
	return user_id
	

# gets username by user-id from the database
def get_by_user_id(user_id):
	sql = "SELECT username FROM users WHERE id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	results = result.fetchone()
	
	username = results[0]
	
	return username
	

# gets user-id by username from the database
def get_by_username(username):
	sql = "SELECT id FROM users WHERE username=:username;"
	result = db.session.execute(sql, {"username":username})
	results = result.fetchone()
	
	user_id = results[0]
	
	return user_id
	

# checks, if username of session is a moderator
def is_moderator(username):
	sql = "SELECT role FROM users WHERE username=:username;"
	result = db.session.execute(sql, {"username":username})
	results = result.fetchone()
	
	user_role = results[0]
	
	
	if (user_role == "moderator"):
		return True
	
	return False
	

# this class includes parameters of a message
class Message_view:
	def __init__(self, msg_id, topic_id, username, content, timestamp, likes):
		self.id = msg_id
		self.topic_id = topic_id
		self.username = username
		self.content = content
		self.timestamp = timestamp
		self.likes = likes
	

# this class includes parameters of a topic
class Topics_view:
	def __init__(self, id, title, timestamp, question_content, user_id):
		self.id = id
		self.title = title
		self.timestamp = timestamp
		self.question_content = question_content
		self.user_id = user_id

	

