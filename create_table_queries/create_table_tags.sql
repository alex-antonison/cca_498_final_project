-- Author: Alex Antonison
-- Create Date: 2018-03-03
-- Description: This creates an external table for the tags stack overflow table that points to my bucket in s3.

-- Change Log
-- User|Date|Change
-- Alex|2018-03-03|Created

create external table tags (
  id int,
  tag string
)
COMMENT 'Tags associate with stack overflow questions'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
location 's3://alex-antonison-data-lake/tags/'