CREATE TABLE IF NOT EXISTS todo(
    id serial,
    title varchar(256),
    content text,
    created timestamp default current_timestamp,
    updated timestamp default current_timestamp,
    state_machine int,
    primary key(id)
);