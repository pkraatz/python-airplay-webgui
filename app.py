from flask import Flask, render_template, request, flash, redirect, url_for
from airplay import AirPlay
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

atv = None

def atv_connect():
    global atv
    atvIP = os.getenv("ATVIP")

    if atv:
        return

    try:
        atv = AirPlay(atvIP)
    except Exception as e:
        print e

@app.route('/')
def index():
    atv_connect()
    global apInfo
    apInfo = atv.server_info()

    global apStatus
    apStatus = atv.playback_info()

    return render_template('index.html', ap_server_info=apInfo, ap_status=apStatus)

@app.route('/action', methods=['POST'])
def play():
    global atv

    if atv:
        if request.form['action'] == "Play":
            atv.play(request.form['videourl'])
            flash('Now playing!')
        elif request.form['action'] == "Pause":
            atv.rate(0.0)
            flash('Paused!')
        elif request.form['action'] == "Resume":
            atv.rate(1.0)
            flash('Resumed!')
        else:
            atv.stop()
            flash('Stopped!')

    return redirect(url_for('index'))

@app.route('/reconnect', methods=['POST'])
def reconnect():
    global atv

    # Reset current connection an start a new one
    atv = None

    flash('Trying reconnect!')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=49913)
