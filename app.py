from flask import Flask, render_template, request, flash, redirect, url_for
from airplay import AirPlay
import os, ConfigParser

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

atv = None

def atv_connect():
    global atv

    if atv:
        return

    atvIP = Config().read("airplay", "device-ip")
    print atvIP

    try:
        atv = AirPlay(atvIP)
    except Exception as e:
        print e

class Config():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'airplay.cfg'))

    def read(self, section, key):
        return self.config.get(section, key)

    def write(self, section, key, value):
        self.config.set(section, key, value)

        # Writing our configuration file
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'airplay.cfg'), 'wb') as configfile:
            self.config.write(configfile)


@app.route('/')
def index():
    atv_connect()

    apStatus = "Disconnected"
    deviceIp = Config().read('airplay', 'device-ip')

    if atv:
        apStatus = "Connected to " + atv.server_info().model

    return render_template('index.html', ap_connection_status=apStatus, device_ip=deviceIp)

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

    flash('Trying to connect...')
    return redirect(url_for('index'))

@app.route('/saveIp', methods=['POST'])
def saveIp():
    global atv
    deviceIp = request.form['device-ip']

    # Reset current connection an start a new one
    atv = None

    Config().write('airplay', 'device-ip', deviceIp)

    flash('IP saved.')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=49913)
