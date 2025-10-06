SET SESSION local_infile = 1;

CREATE TABLE IF NOT EXISTS obrigacoes_com_data (
  obligation_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(500),
  notes TEXT,
  date DATE,
  jurisdiction_level VARCHAR(50),
  jurisdiction VARCHAR(200),
  state VARCHAR(10),
  county VARCHAR(100),
  city VARCHAR(100),
  category VARCHAR(100),
  frequency VARCHAR(50),
  sources JSON
);

CREATE TABLE IF NOT EXISTS obrigacoes_sem_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(500),
  notes TEXT
);

TRUNCATE TABLE obrigacoes_sem_data;
TRUNCATE TABLE obrigacoes_com_data;

LOAD DATA LOCAL INFILE 'C:/87project/Tax_CalendarX/obrigacoes_com_data.csv'
INTO TABLE obrigacoes_com_data
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(title, notes, date, jurisdiction_level, jurisdiction, state, county, city, category, frequency, sources);

LOAD DATA LOCAL INFILE 'C:/87project/Tax_CalendarX/obrigacoes_sem_data.csv'
INTO TABLE obrigacoes_sem_data
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(title, notes);
