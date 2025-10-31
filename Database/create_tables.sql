-- 1. Create a dedicated tablespace
CREATE TABLESPACE users
  DATAFILE '/opt/oracle/oradata/FREE/users.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED
  EXTENT MANAGEMENT LOCAL;

-- 2. Create the schema/user
CREATE USER paymentus IDENTIFIED BY paymentusp
  DEFAULT TABLESPACE users
  TEMPORARY TABLESPACE temp
  QUOTA UNLIMITED ON users;

-- 3. Grant privileges
GRANT CONNECT, RESOURCE TO paymentus;

-- 4. Connect as new user
-- sql paymentus/paymentusp@//localhost:1521/FREEPDB1

-- 5. Create tables
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    user_name VARCHAR2(255),
    last_login_date DATE,
    created_on DATE
);

CREATE TABLE liability (
    liability_id NUMBER PRIMARY KEY,
    account_number NUMBER,
    account_status VARCHAR2(50),
    amount_due NUMBER(20,2),
    amount_paid NUMBER(20,2),
    amount_past_due DATE,
    city VARCHAR2(100),
    country VARCHAR2(100),
    cutoff_date DATE,
    due_date DATE,
    effective_date DATE,
    payment_type VARCHAR2(50),
    min_amount NUMBER(20,2),
    max_amount NUMBER(20,2)
);

CREATE TABLE payment_method (
    payment_method_id NUMBER PRIMARY KEY,
    account_number VARCHAR2(50),
    active_flag VARCHAR2(1),
    card_holder_name VARCHAR2(255),
    expiry_date DATE,
    payment_method_type_code VARCHAR2(50),
    save_for_reuse_flag VARCHAR2(1)
);

CREATE TABLE payments (
    payment_amount NUMBER(20,2),
    payment_reference_number NUMBER,
    user_id NUMBER,
    liability_id NUMBER,
    channel_code VARCHAR2(50),
    payment_method_id NUMBER,
    submitted_date DATE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_liability FOREIGN KEY (liability_id) REFERENCES liability(liability_id),
    CONSTRAINT fk_payment_method FOREIGN KEY (payment_method_id) REFERENCES payment_method(payment_method_id)
);
