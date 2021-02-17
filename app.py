from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO, join_room
import sqlite3
import setup_db
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
socketio = SocketIO(app)


@app.route('/')
@app.route('/home')
def home():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return render_template("chat.html", username=session.get('username'), color=session.get('color'))


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        try:
            username = request.form['username']
            color = request.form['color']

            if username and not username.isspace():
                with sqlite3.connect('data.db') as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO User (Username) VALUES(?);", (username,))
                    con.commit()

                    session['logged_in'] = True
                    session['username'] = username
                    session['color'] = color

                    return home()
            else:
                flash("Please enter a valid username")
        except:
            con.rollback()
            flash("Error logging in")
        finally:
            return home()


@app.route('/log_out')
def log_out():
    socketio.emit('log_out_announcement', session.get('username'))
    session['username'] = ""
    session['logged_in'] = False
    return home()


@socketio.on('join_room')
def handle_join_room(data):
    app.logger.info("{} has joined the room.".format(data['username']))
    join_room(data['username'])
    return socketio.emit('join_room_announcement', data)


@socketio.on('send_message')
def handle_send_message(data):
    app.logger.info("{} has sent a message to the room: {}".format(data['username'], data['message']))

    return socketio.emit('receive_message', data)


if __name__ == '__main__':
    socketio.run(app)
