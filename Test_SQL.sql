-- Create a sample table
CREATE TABLE SampleTable (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Country VARCHAR(50),
    RegistrationDate DATE
);

-- Insert 5 rows into the sample table
INSERT INTO SampleTable (ID, Name, Age, Country, RegistrationDate)
VALUES
    (1, 'Alice', 30, 'USA', '2024-01-15'),
    (2, 'Bob', 25, 'Canada', '2024-02-20'),
    (3, 'Charlie', 35, 'UK', '2024-03-10'),
    (4, 'Diana', 28, 'Australia', '2024-04-05'),
    (5, 'Ethan', 40, 'Germany', '2024-05-25');

-- Verify the inserted rows
SELECT * FROM SampleTable;
