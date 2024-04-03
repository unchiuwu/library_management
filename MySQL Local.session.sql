create table if not exists users (
    userid int auto_increment primary key, 
    username varchar (50) unique, 
    password varchar (50) not null, 
    admin boolean default 0, 
    total_books_borrowed int
);

create table if not exists books ( 
    bookid int auto_increment primary key,
    title varchar(255),
    author varchar(255),
    no_of_copies int,
    availability boolean default 0,
    borrowed_count int
);

create table if not exists transactions (
    transactionid int auto_increment primary key, 
    bookid int unique, 
    title varchar(255), 
    username varchar(50), 
    date_issued timestamp default current_timestamp, 
    due_date timestamp default (date_add(date_issued, INTERVAL 14 DAY)),
    return_date timestamp null default null, 
    late_fees int default 0,
    foreign key (bookid) references books(bookid)
);

create table fees(
    feeid int auto_increment primary key,
    transactionid int,
    userid int,
    title varchar(255),
    date_issued timestamp,
    date_returned timestamp,
    overdue int,
    feeamt int,
    foreign key (transactionid) references transactions(transactionid)
);

