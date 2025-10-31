docker  run -d -p 1521:1521 --name oracle-db container-registry.oracle.com/database/free:latest-lite

docker exec -it oracle-db bash

sqlplus / as sysdba

CREATE TABLESPACE users DATAFILE '/opt/oracle/oradata/FREE/users.dbf' SIZE 100M AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED EXTENT MANAGEMENT LOCAL;

CREATE USER paymentus IDENTIFIED BY paymentusp  DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp  QUOTA UNLIMITED ON users;

GRANT CONNECT, RESOURCE TO paymentus;

exit;

sql paymentus/paymentusp@//localhost:1521/FREEPDB1

