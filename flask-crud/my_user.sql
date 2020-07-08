create table test_db.my_user(
	id int(11) NOT NULL auto_increment,
	user_name varchar(20),
	created_at datetime default current_timestamp,
	udpated_at datetime default current_timestamp,
	primary key(id)
);