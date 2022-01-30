Create database email_validation_schema;
Use email_validation_schema;

Create table users (
	id int primary key auto_increment,
    email varchar(100),
    created_at datetime,
    updated_at datetime
);