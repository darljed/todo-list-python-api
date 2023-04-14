import sqlite3,binascii,os,base64
from datetime import datetime, timedelta
from config import AUTH_URLS, TASK_URLS, SETTINGS
from flask import abort

class Connection:
    def __init__(self):
        self.connection = sqlite3.connect("todolist.db")


class User:
    def __init__(self):
        self.connection = Connection().connection

    def get_user_count_byusername(self,username):
        cur = self.connection.cursor()
        result = cur.execute("SELECT COUNT(username) FROM users WHERE (`username`='{0}');".format(username))
        count = cur.fetchone()[0]
        return count

    def get_user_details_byusername(self,username):
        cur = self.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE (`username`='{0}');".format(username)).fetchall()
        return result

    def user_exists(self,username):
        if(self.get_user_count_byusername(username) > 0):
            return True
        else:
            return False

    def create_user(self,username,password):
        
        if not self.user_exists(username):
            # encode password 
            password = base64.b64encode(password.encode("ascii","strict"))  
            cur = self.connection.cursor()
            cur.execute("INSERT INTO users (username,password) VALUES (?, ?) ",
            (username,password))
            self.connection.commit()

            return {'message':{
                'status': 'success',
                'content':'New user has been created.',
                'login_url': '/auth/login'
            },
            'code':201}
        else:
            return {'message':{
                'status': 'failed',
                'content':'The username already exists. Please select a different username.',
            },
            'code':200}

    def user_login(self,username,password):
        
        if self.user_exists(username):
            user = self.get_user_details_byusername(username)
            user_id=user[0][0]
            dbusername=user[0][1]
            dbpassword=base64.b64decode(user[0][2])
            dbpassword=dbpassword.decode('ascii','strict')

            if(password == dbpassword):
                #login successfull
                self.s = Session(user_id)
                return {
                    'status': 'success',
                    'session_key': self.s.get_sessionkey(),
                    'urls': TASK_URLS
                }
        return False

class Session:
    def __init__(self,user_id=None):
        self.connection = Connection().connection
        self.user_id = user_id

    def validate_sessionkey(self,session_key):
        cur = self.connection.cursor()
        session_info = cur.execute("SELECT session_id,expires_at,user_id FROM sessions WHERE (`session_key`=? AND `status`='active')",(session_key,)).fetchall()

        if len(session_info) < 1:
            return False
        else:

            # check status validity
            if(self.session_expired(session_info[0][1])):
                self.session_exp_update(session_info[0][0],True)
                return False
            else:
                self.session_exp_update(session_info[0][0],False)
                return {
                    'session_id': session_info[0][0],
                    'expires_at': session_info[0][1],
                    'user_id': session_info[0][2]
                }

    def get_sessionkey(self):
        # check if user has active session
        cur = self.connection.cursor()
        result = cur.execute("SELECT session_id,session_key,expires_at FROM sessions WHERE (`user_id`=? AND `status`='active')",(self.user_id,)).fetchall()
        if(len(result) > 0):
            # return existing session key and update expiration time
            sid = result[0][0]
            skey = result[0][1]
            expires_at = result[0][2]

            isExpired = self.session_expired(expires_at)
            self.session_exp_update(sid,isExpired)
            if(isExpired):
                return self.new_sessionkey()
            else:
                return skey
        else:
            return self.new_sessionkey()

    def has_duplicate(self,session_key):
        cur = self.connection.cursor()
        cur.execute('SELECT COUNT(session_id) FROM sessions WHERE (`session_key`=?)',(session_key,))
        count = cur.fetchone()[0]
        if count > 0:
            return True
        return False

    def new_sessionkey(self):
        new_skey = None
        duplicate = True
        while(duplicate):
            new_skey = binascii.hexlify(os.urandom(24)).decode() 

            if(self.has_duplicate(new_skey)):
                duplicate = True
                print("Session Key has duplicates")
            else: 
                duplicate = False
        cur = self.connection.cursor()
        cur.execute('INSERT INTO sessions (user_id,session_key,expires_at,status) VALUES (?, ?, ?, ?)',
        (self.user_id, new_skey, self.newExpTime(), 'active'))
        self.connection.commit()

        return new_skey

    def session_exp_update(self,session_id,isExpired):
        
        cur = self.connection.cursor()
        if(isExpired):
            cur.execute('UPDATE sessions SET status = "expired" WHERE session_id=?',(session_id,))
            cur.connection.commit()
        else:
            #set new expiration time
            currentdt = self.newExpTime()

            cur.execute('UPDATE sessions SET expires_at = ? WHERE session_id=?',(currentdt,session_id))
            cur.connection.commit()

    def session_expired(self,expires_at):
        now = datetime.now()
        exp = datetime.strptime(expires_at,'%Y-%m-%d %H:%M:%S')
        if(now>=exp):
            return True
        else:
            return False

    def newExpTime(self):
        currentdt = datetime.now() + timedelta(minutes=SETTINGS['session']['duration_mins'])
        return currentdt.strftime('%Y-%m-%d %H:%M:%S')

class Task:
    def __init__(self, user_id):
        self.connection = Connection().connection
        self.user_id = user_id

    def get_tasks(self):
        cur = self.connection.cursor()
        tasks = cur.execute('SELECT task_id, task FROM tasks WHERE (user_id=?)',(self.user_id,)).fetchall()
        return tasks

class Auth:
    def __init__(self,request):
        self.request = request
        self.connection = Connection().connection
        
    def validate(self):
        auth_token = self.request.headers.get('Authorization')
        if(not auth_token):
            abort(403)
        if(not "Key " in auth_token):
            abort(403)

        session_key = auth_token.replace('Key ','')

        # check if session key exists. 
        session_key_details = Session().validate_sessionkey(session_key)
        if(session_key_details):
            user_id = session_key_details['user_id']
            return user_id
        else:
            abort(403)
        


        # headers = request.headers.get('Content-Type')
        # test = request.form.get('test')
        # auth = request.headers.get('Authorization')



if __name__ == "__main__":
    conn = Connection()
    conn.db_init()