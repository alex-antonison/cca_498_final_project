-- Author: Alex Antonison
-- Create Date: 2018-03-03
-- Description: This creates an external table that points to my bucket in s3 with the quesitons.

-- Change Log
-- User|Date|Change
-- Alex|2018-03-03|Created

create external table questions (
  id int,
  owner_user_id int,
  creation_date timestamp,
  score int,
  title string,
  body string
)
COMMENT 'Stack overflow questions'
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   'separatorChar' = ',',
   'quoteChar' = '\"',
   'escapeChar' = '\\'
   )
STORED AS TEXTFILE
location 's3://alex-antonison-data-lake/questions/'