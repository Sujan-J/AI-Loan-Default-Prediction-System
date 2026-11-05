CREATE DATABASE IF NOT EXISTS loan_prediction;
USE loan_prediction;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('user','admin') NOT NULL DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prediction_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  age INT, annual_income DECIMAL(14,2), employment_type VARCHAR(50),
  education VARCHAR(50), marital_status VARCHAR(30), dependents INT,
  loan_amount DECIMAL(14,2), loan_term INT, credit_score INT,
  existing_debt DECIMAL(14,2), loan_purpose VARCHAR(50),
  prediction VARCHAR(30) NOT NULL, confidence DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
