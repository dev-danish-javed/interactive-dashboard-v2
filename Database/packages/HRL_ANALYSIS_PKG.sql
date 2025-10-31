create or replace PACKAGE HRL_ANALYSIS_PKG AS

    HRL_THRESHOLD CONSTANT NUMBER := 10000;

    FUNCTION GET_HIGH_RISK_COUNT
        RETURN NUMBER;

    PROCEDURE GET_HIGH_RISK_LIST (
        p_hrl_list OUT HRL_CUSTOMER_LIST
    );

END HRL_ANALYSIS_PKG;
/

create or replace PACKAGE BODY HRL_ANALYSIS_PKG AS

    -- Function 1 Implementation: Get High-Risk Liability Customer Count
    FUNCTION GET_HIGH_RISK_COUNT
        RETURN NUMBER
    IS
        v_hrl_count NUMBER := 0;
    BEGIN
        -- Final Corrected Join Path: USERS -> PAYMENTS -> LIABILITY -> PAYMENT_METHOD
        SELECT COUNT(DISTINCT u.USER_ID)
        INTO v_hrl_count
        FROM USERS u
        JOIN PAYMENTS pm ON u.USER_ID = pm.USER_ID -- Link User to Payments
        JOIN LIABILITY l ON pm.LIABILITY_ID = l.LIABILITY_ID -- Link Payments to Liability record
        JOIN PAYMENT_METHOD p ON l.ACCOUNT_NUMBER = p.ACCOUNT_NUMBER -- Link Liability to Payment Method

        WHERE (l.AMOUNT_DUE - l.AMOUNT_PAID) >= HRL_THRESHOLD -- Condition 1: Financial Stress (>= 10,000)
          AND p.ACTIVE_FLAG = 'X'; -- Condition 2: Payment Volatility (Inactive status 'X')

        RETURN v_hrl_count;

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 0;
    END GET_HIGH_RISK_COUNT;


    -- Procedure 2 Implementation: Get High-Risk Liability Customer List
    PROCEDURE GET_HIGH_RISK_LIST (
        p_hrl_list OUT HRL_CUSTOMER_LIST
    )
    IS
    BEGIN
        p_hrl_list := HRL_CUSTOMER_LIST();

        -- Corrected Join Path for Bulk Collect
        SELECT HRL_CUSTOMER_TYPE(
            u.USER_ID,
            u.USER_NAME,
            (l.AMOUNT_DUE - l.AMOUNT_PAID), 
            p.ACTIVE_FLAG 
        )
        BULK COLLECT INTO p_hrl_list
        FROM USERS u
        JOIN PAYMENTS pm ON u.USER_ID = pm.USER_ID
        JOIN LIABILITY l ON pm.LIABILITY_ID = l.LIABILITY_ID
        JOIN PAYMENT_METHOD p ON l.ACCOUNT_NUMBER = p.ACCOUNT_NUMBER

        WHERE (l.AMOUNT_DUE - l.AMOUNT_PAID) >= HRL_THRESHOLD
          AND p.ACTIVE_FLAG = 'X';

    EXCEPTION
        WHEN OTHERS THEN
            p_hrl_list := HRL_CUSTOMER_LIST();
    END GET_HIGH_RISK_LIST;

END HRL_ANALYSIS_PKG;
