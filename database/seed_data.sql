
USE QA_Automation_DB;
GO

-- Checkout customer data
INSERT INTO dbo.TestCustomers
    (TestCaseID, FirstName, LastName, PostalCode)
SELECT 'TC_CHECKOUT_001', 'John', 'Test', 'N2J2K2'
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestCustomers
    WHERE TestCaseID = 'TC_CHECKOUT_001'
);

INSERT INTO dbo.TestCustomers
    (TestCaseID, FirstName, LastName, PostalCode)
SELECT 'TC_CHECKOUT_002', 'Sarah', 'Smith', 'M5V2T6'
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestCustomers
    WHERE TestCaseID = 'TC_CHECKOUT_002'
);

INSERT INTO dbo.TestCustomers
    (TestCaseID, FirstName, LastName, PostalCode)
SELECT 'TC_CHECKOUT_003', 'David', 'Kumar', 'L5B3C4'
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestCustomers
    WHERE TestCaseID = 'TC_CHECKOUT_003'
);

-- Product price data
INSERT INTO dbo.TestProducts
    (ProductName, ExpectedPrice)
SELECT 'Sauce Labs Backpack', 29.99
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestProducts
    WHERE ProductName = 'Sauce Labs Backpack'
);

INSERT INTO dbo.TestProducts
    (ProductName, ExpectedPrice)
SELECT 'Sauce Labs Bolt T-Shirt', 15.99
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestProducts
    WHERE ProductName = 'Sauce Labs Bolt T-Shirt'
);

INSERT INTO dbo.TestProducts
    (ProductName, ExpectedPrice)
SELECT 'Sauce Labs Bike Light', 9.99
WHERE NOT EXISTS (
    SELECT 1 FROM dbo.TestProducts
    WHERE ProductName = 'Sauce Labs Bike Light'
);
GO
