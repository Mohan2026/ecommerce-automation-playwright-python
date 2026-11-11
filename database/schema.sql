
IF DB_ID('QA_Automation_DB') IS NULL
BEGIN
    CREATE DATABASE QA_Automation_DB;
END;
GO

USE QA_Automation_DB;
GO

IF OBJECT_ID('dbo.TestCustomers', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.TestCustomers (
        CustomerID INT IDENTITY(101,1) PRIMARY KEY,
        TestCaseID VARCHAR(30) NOT NULL UNIQUE,
        FirstName VARCHAR(50) NOT NULL,
        LastName VARCHAR(50) NOT NULL,
        PostalCode VARCHAR(15) NOT NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
END;
GO

IF OBJECT_ID('dbo.TestProducts', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.TestProducts (
        ProductID INT IDENTITY(1,1) PRIMARY KEY,
        ProductName VARCHAR(100) NOT NULL UNIQUE,
        ExpectedPrice DECIMAL(10,2) NOT NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
END;
GO
