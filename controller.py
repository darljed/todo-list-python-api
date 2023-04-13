import sqlite3,binascii,os,base64
from datetime import datetime, timedelta
from config import AUTH_URLS, TASK_URLS

class Connection:
    def __init__(self):
        self.connection = sqlite3.connect("todolist.db")


class User(Connection):
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

            return {
                'status': 'success',
                'content':'New user has been created.',
                'login_url': '/auth/login'
            }
        else:
            return 'The username already exists. Please select a different username.'

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

class Session(Connection):
    def __init__(self,user_id):
        self.connection = Connection().connection
        self.user_id = user_id

    def get_sessionkey(self):

        '''
        Todo:
        Add algorithm to check expiration of session key
        Check if session key exists in db
        Save new session key to db with user_id
        set expiration date and status
        '''
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
        currentdt = datetime.now() + timedelta(minutes=10)
        return currentdt.strftime('%Y-%m-%d %H:%M:%S')



        



if __name__ == "__main__":
    conn = Connection()
    conn.db_init()