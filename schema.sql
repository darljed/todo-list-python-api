DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sessions;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    sort_index INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE sessions (
    "session_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL,
    "session_key" TEXT NOT NULL,
    "expires_at" DATETIME NOT NULL,
    "status" TEXT NOT NULL DEFAULT active,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);


-- Users 
INSERT INTO users (username,password) VALUES ("test1","cGFzc3dvcmQx");
INSERT INTO users (username,password) VALUES ("test2","cGFzc3dvcmQy");

-- Tasks 

INSERT INTO tasks (task,sort_index,user_id) VALUES ("buy milk",0,1);
INSERT INTO tasks (task,sort_index,user_id) VALUES ("create proposal for client A",1,1);
INSERT INTO tasks (task,sort_index,user_id) VALUES ("water the plants",2,1);