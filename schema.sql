DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS post;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(20) NOT NULL,
  roleId INT NOT NULL,
  firstname VARCHAR(30),
  lastname VARCHAR(30),
  UNIQUE KEY usernameIndex (username)
);

# SAMPLE DATA
# TO DO -
# store password hashes
INSERT INTO users(username, password, roleId, firstname, lastname)
VALUES ("admin", "admin", 1, "Administrator", NULL);

INSERT INTO users(username, password, roleId, firstname, lastname)
VALUES ("user", "pass", 2, "Brian", "Karabinchak");

CREATE TABLE post (
	id INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	link text,
	content VARCHAR(1000),
    createdTime DATETIME CURRENT_TIMESTAMP,
    modifiedTime DATETIME ON UPDATE CURRENT_TIMESTAMP
);