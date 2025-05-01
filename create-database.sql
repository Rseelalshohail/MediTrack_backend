CREATE DATABASE meditrack;

CREATE USER meditrack_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE meditrack TO meditrack_admin;
