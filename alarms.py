#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from flask import Flask, render_template
app = Flask(__name__)


def get_db_data():
    conn = psycopg2.connect(dbname="mcu", user="user", host="localhost", password="user")
    cur = conn.cursor()
    sql_cmd = "SELECT * FROM alarm_hist \
                WHERE id > (SELECT max(id) FROM alarm_hist) - 2000;"
    cur.execute(sql_cmd)
    result_raw = cur.fetchall()
    conn.close()
    if len(result_raw) > 0:
        result_raw.sort( reverse=True)
        return result_raw
    else:
        return []

@app.route('/')
def index():
    alarms = get_db_data()
    return render_template('index.html', alarms=alarms)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
