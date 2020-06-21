create table user_table(
    id int(5) not null auto_increment,
    user_name varchar(20) not null,
    password varchar(100) not null,
    bio varchar(256) default null,
    created_at datetime default current_timestamp,
    last_login datetime default null,
    PRIMARY KEY (id,user_name)
);