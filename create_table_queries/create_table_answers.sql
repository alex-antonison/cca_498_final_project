-- Author: Alex Antonison
-- Create Date: 2018-03-03
-- Description: This creates an external table that points to my bucket in s3 with the answers file.

-- Change Log
-- User|Date|Change
-- Alex|2018-03-03|Created


create external table answers (
  id int,
  owner_user_id int,
  creation_date timestamp,
  parent_id int,
  score int,
  body string
)
COMMENT 'Stack overflow answers'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
location 's3://alex-antonison-data-lake/answers/'