create table contest
(
    id          varchar(30)  not null
        primary key,
    platform    varchar(15)  not null,
    contestname varchar(100) null,
    starttime   varchar(25)  null,
    endtime     varchar(25)  null,
    link        varchar(100) null,
    count       int          null,
    teamcontest int          null,
    deleted     int          not null
);

