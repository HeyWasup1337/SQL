import mysql.connector
import hashlib
from flask import Flask, render_template, request
from termcolor import colored

app = Flask(__name__)

# Подключение к базе данных MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ZADANIE"
)

mycursor = mydb.cursor()

# Создание таблицы пользователей, если она не существует
mycursor.execute("CREATE TABLE IF NOT EXISTS ZADANIE(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

def register_user(user_name, user_password):
    mycursor.execute("SELECT * FROM ZADANIE WHERE username=%s", (user_name,))
    if mycursor.fetchone():
        return colored("Пользователь существует", "red")
    else:
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        mycursor.execute("INSERT INTO ZADANIE (username, password) VALUES (%s, %s)", (user_name, user_password))
        mydb.commit()
        return colored("Вы зарегистрированы", "green")

def login_user(user_name, user_password):
    user_password = hashlib.sha256(user_password.encode()).hexdigest()
    mycursor.execute("SELECT * FROM ZADANIE WHERE username=%s AND password=%s", (user_name, user_password))
    user = mycursor.fetchone()
    if user:
        return colored(f"Добро пожаловать, {user_name}!", "green")
    else:
        return colored("Неправильный логин или пароль", "red")

def get_all_users():
    mycursor.execute("SELECT username FROM ZADANIE")
    users = mycursor.fetchall()
    return [user[0] for user in users]

# Главная страница с формой регистрации и входа
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'register' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            message = register_user(user_name, user_password)
        elif 'login' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            message = login_user(user_name, user_password)
    else:
        message = None
    users = get_all_users()
    return render_template('index.html', message=message, users=users)

if __name__ == "__main__":
    app.run(debug=True)
