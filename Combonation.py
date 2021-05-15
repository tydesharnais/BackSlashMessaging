import sqlite3

username = input('Enter your Username: ')
with sqlite3.connect('waldo.db') as db:
    cursor = db.cursor()
    find_user = ("SELECT * FROM user WHERE username = ?")
    cursor.execute(find_user, [(username)])
    results = cursor.fetchall()
    for row in results:
        print(row[6])
    np = input('Enter your New Password: ')
    new_pass = ("UPDATE user SET password = ? WHERE username = ?")
    cursor.execute(new_pass, [(np), (username)])
    db.commit()
    cursor.execute('SELECT * FROM user')
    passresults = cursor.fetchall()
    for row in passresults:
        print(row)
