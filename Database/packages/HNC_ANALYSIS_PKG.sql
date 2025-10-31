create or replace PACKAGE HNC_ANALYSIS_PKG AS

    -- Constant: The minimum payment threshold to qualify as an HNC (500,000 units/rupees).
    HNC_THRESHOLD CONSTANT NUMBER := 500000;

    -- [REMOVED] IS_HIGH_NET_WORTH (BOOLEAN) to simplify logic.

    -- [NEW] This is the core HNC check function, now returns a NUMBER (1 or 0) for SQL-safety.
    FUNCTION IS_HNC_SQL_WRAPPER (p_user_id IN NUMBER)
        RETURN NUMBER;

    -- Function 1: Returns the count of HNCs who have "exited" (inactive).
    FUNCTION GET_EXITED_HNC_COUNT (p_cutoff_days IN NUMBER DEFAULT 180)
        RETURN NUMBER;

    -- Procedure 2: Returns a list of HNCs who have exited.
    PROCEDURE GET_EXITED_HNC_LIST (
        p_cutoff_days IN NUMBER DEFAULT 180,
        p_hnc_list OUT HNC_CUSTOMER_LIST
    );

END HNC_ANALYSIS_PKG;

/

create or replace PACKAGE BODY HNC_ANALYSIS_PKG AS

    -- [NEW] HNC Check Function (SQL-safe): Returns 1 if HNC, 0 otherwise.
    FUNCTION IS_HNC_SQL_WRAPPER (p_user_id IN NUMBER)
        RETURN NUMBER
    IS
        v_total_payment NUMBER;
    BEGIN
        -- Calculate total payment amount from the PAYMENTS table for the user
        SELECT SUM(NVL(p.PAYMENT_AMOUNT, 0))
        INTO v_total_payment
        FROM PAYMENTS p
        WHERE p.USER_ID = p_user_id;

        -- Check if total payment exceeds the HNC threshold (500,000)
        IF v_total_payment > HNC_THRESHOLD THEN
            RETURN 1; -- HNC
        ELSE
            RETURN 0; -- Not HNC
        END IF;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0; -- No payments, so not HNC
        WHEN OTHERS THEN
            RETURN 0;
    END IS_HNC_SQL_WRAPPER;


    -- Function 1 Implementation: Get Exited HNC Count
    FUNCTION GET_EXITED_HNC_COUNT (p_cutoff_days IN NUMBER DEFAULT 180)
        RETURN NUMBER
    IS
        v_exited_count NUMBER := 0;
    BEGIN
        -- Count customers who meet BOTH criteria: Inactivity AND High Net Worth (using the SQL-safe function)
        SELECT COUNT(u.USER_ID)
        INTO v_exited_count
        FROM USERS u
        WHERE u.LAST_LOGIN_DATE < (SYSDATE - p_cutoff_days) -- Inactivity/Exit Criteria
        AND HNC_ANALYSIS_PKG.IS_HNC_SQL_WRAPPER(u.USER_ID) = 1; -- HNC Criteria (SQL-safe check)

        RETURN v_exited_count;

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 0;
    END GET_EXITED_HNC_COUNT;

    -- Procedure 2 Implementation: Get Exited HNC List
    PROCEDURE GET_EXITED_HNC_LIST (
        p_cutoff_days IN NUMBER DEFAULT 180,
        p_hnc_list OUT HNC_CUSTOMER_LIST
    )
    IS
    BEGIN
        -- Initialize the output collection
        p_hnc_list := HNC_CUSTOMER_LIST();

        -- Bulk collect the data into the structured HNC_CUSTOMER_LIST type
        SELECT HNC_CUSTOMER_TYPE(
            u.USER_ID,
            u.USER_NAME,
            (SELECT SUM(NVL(p.PAYMENT_AMOUNT, 0)) FROM PAYMENTS p WHERE p.USER_ID = u.USER_ID), -- Recalculate total payment for output
            u.LAST_LOGIN_DATE
        )
        BULK COLLECT INTO p_hnc_list
        FROM USERS u
        WHERE u.LAST_LOGIN_DATE < (SYSDATE - p_cutoff_days)
        AND HNC_ANALYSIS_PKG.IS_HNC_SQL_WRAPPER(u.USER_ID) = 1;

    EXCEPTION
        WHEN OTHERS THEN
            p_hnc_list := HNC_CUSTOMER_LIST(); -- Return empty list on error
    END GET_EXITED_HNC_LIST;

END HNC_ANALYSIS_PKG;
