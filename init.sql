CREATE DATABASE IF NOT EXISTS balance;

USE balance;

CREATE TABLE IF NOT EXISTS balances (
  account_id VARCHAR(255) PRIMARY KEY,
  balance DECIMAL(10, 2) NOT NULL
);
