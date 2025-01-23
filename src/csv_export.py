import subprocess

users = "sqlite3 -header -csv db.sqlite3 \"select * from users;\" > users.csv"
tests = "sqlite3 -header -csv db.sqlite3 \"select * from tests;\" > tests.csv"
subprocess.run(users, shell=True)
subprocess.run(tests, shell=True)

