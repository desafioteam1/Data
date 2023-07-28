import pymysql
import os
from dotenv import load_dotenv

# Load API keys from the environment variables
load_dotenv()

# Get API keys from the environment variables
username = os.getenv("username")
password = os.getenv("password")

# Database details and connection
host = "db-heat.calrvam3hyef.eu-north-1.rds.amazonaws.com"
port = 3306

# Establish a connection to the database
db = pymysql.connect(
    host=host,
    user=username,
    password=password,
    cursorclass=pymysql.cursors.DictCursor
)

# Create a cursor to execute queries on the database
cursor = db.cursor()

# Create the "heat_energy" database
create_db = '''CREATE DATABASE heat_energy'''
cursor.execute(create_db)

# Commit the changes to the database
cursor.connection.commit()

# Select the newly created database for use
use_db = '''USE heat_energy'''
cursor.execute(use_db)

# Create the "users" table
create_table = '''
CREATE TABLE users (
  user_id int NOT NULL PRIMARY KEY,
  first_name varchar(45) NOT NULL,
  surname varchar(100),
  email varchar(45) NOT NULL UNIQUE,
  user_position varchar(45) NOT NULL,
  hashed_password varchar(200) NOT NULL,
  admin boolean NOT NULL,
  logged boolean NOT NULL
)
'''
cursor.execute(create_table)

# Create the "account" table
create_table = '''
CREATE TABLE account (
  user_id int,
  account_holder varchar(200) NOT NULL,
  account_number varchar(200) NOT NULL UNIQUE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
'''
cursor.execute(create_table)

# Create the "buildings" table
create_table = '''
CREATE TABLE buildings (
  user_id serial,
  address_number INT NOT NULL,
  street VARCHAR(100) NOT NULL,
  postal_code VARCHAR(10) NOT NULL,
  city VARCHAR(100) NOT NULL,
  province VARCHAR(100) NOT NULL,
  autonomous_community VARCHAR(100) NOT NULL,
  cif VARCHAR(12) NOT NULL UNIQUE,
  total_area INT NOT NULL,
  communal_areas_area INT NOT NULL,
  housing_area INT NOT NULL,
  number_of_apartments INT NOT NULL,
  year_of_construction INT NOT NULL,
  cadastre_number VARCHAR(100) NOT NULL UNIQUE,
  energy_efficiency_certificate VARCHAR(100),
  project_state VARCHAR(50) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
'''
cursor.execute(create_table)