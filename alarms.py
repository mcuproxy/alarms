#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from jinja2 import Template


def get_db_data():
    conn = psycopg2.connect(dbname="mcu", user="user", host="localhost", password="user")
    cur = conn.cursor()
    sql_cmd = "SELECT * FROM alarm_hist \
                WHERE id > (SELECT max(id) FROM alarm_hist) - 1000;"
    cur.execute(sql_cmd)
    result_raw = cur.fetchall()
    conn.close()
    if len(result_raw) > 0:
        result_raw.sort( reverse=True)
        return result_raw
    else:
        return []

def make_index():
    alarms = get_db_data()
    
    with open("template.html", 'r') as f:
        template = Template(f.read())
        
    with open("index.html", 'w') as f:
        f.write(template.render(alarms=alarms))

if __name__ == '__main__':
    make_index()
