-- 1. Insert users
BEGIN
  FOR i IN 1..5 LOOP
    INSERT INTO users (user_id, user_name, last_login_date, created_on)
    VALUES (
      i,
      'User_' || i,
      SYSDATE - DBMS_RANDOM.VALUE(0,30),
      SYSDATE - DBMS_RANDOM.VALUE(30,365)
    );
  END LOOP;
  COMMIT;
END;
/

-- 2. Insert liabilities
BEGIN
  FOR i IN 1..5 LOOP
    INSERT INTO liability (
      liability_id, account_number, account_status, amount_due, amount_paid, amount_past_due,
      city, country, cutoff_date, due_date, effective_date, payment_type, min_amount, max_amount
    ) VALUES (
      i,
      100000 + i,
      CASE WHEN MOD(i,2)=0 THEN 'ACTIVE' ELSE 'INACTIVE' END,
      ROUND(DBMS_RANDOM.VALUE(1000,5000),2),
      ROUND(DBMS_RANDOM.VALUE(0,1000),2),
      SYSDATE - DBMS_RANDOM.VALUE(0,30),
      'City_' || i,
      'Country_' || i,
      SYSDATE + 15,
      SYSDATE + 30,
      SYSDATE - 10,
      CASE WHEN MOD(i,2)=0 THEN 'FULL' ELSE 'PARTIAL' END,
      ROUND(DBMS_RANDOM.VALUE(100,500),2),
      ROUND(DBMS_RANDOM.VALUE(500,1000),2)
    );
  END LOOP;
  COMMIT;
END;
/

-- 3. Insert payment methods
BEGIN
  FOR i IN 1..5 LOOP
    INSERT INTO payment_method (
      payment_method_id, account_number, active_flag, card_holder_name, expiry_date,
      payment_method_type_code, save_for_reuse_flag
    ) VALUES (
      i,
      'ACC' || (1000+i),
      CASE WHEN MOD(i,2)=0 THEN 'Y' ELSE 'N' END,
      'Holder_' || i,
      ADD_MONTHS(SYSDATE, 12),
      CASE WHEN MOD(i,2)=0 THEN 'CARD' ELSE 'BANK' END,
      CASE WHEN MOD(i,2)=0 THEN 'Y' ELSE 'N' END
    );
  END LOOP;
  COMMIT;
END;
/

-- 4. Insert 20 payments
BEGIN
  FOR i IN 1..20 LOOP
    INSERT INTO payments (
      payment_amount,
      payment_reference_number,
      user_id,
      liability_id,
      channel_code,
      payment_method_id,
      submitted_date
    ) VALUES (
      ROUND(DBMS_RANDOM.VALUE(100, 10000), 2),
      i + 1000,
      MOD(i-1,5)+1,
      MOD(i-1,5)+1,
      CASE WHEN MOD(i,2)=0 THEN 'WEB' ELSE 'APP' END,
      MOD(i-1,5)+1,
      SYSDATE - DBMS_RANDOM.VALUE(0,30)
    );
  END LOOP;
  COMMIT;
END;
/