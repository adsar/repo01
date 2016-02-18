
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--group the n-triples by object column
objects = group ntriples by (object) PARALLEL 50;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
count_by_object = foreach objects generate flatten($0), COUNT($1) as count PARALLEL 50;
DESCRIBE count_by_object;

========================================================================
-- Question 1: how many records are there in count_by_object?
---------------------------------------------------------------
-- Project just one field per record
record_group = FOREACH count_by_object GENERATE group;
DESCRIBE record_group;

-- Put all the records into a single bag so we can count
all_record_group = GROUP record_group ALL;
DESCRIBE all_record_group;


-- count - equivalent to FOREACH all_record_group GENERATE COUNT(record_group);
-- (don't need parallel reducers)
record_count = FOREACH all_record_group GENERATE COUNT_STAR(record_group);
DESCRIBE record_count;

------------------------------------------------------------------------
--sh hdfs dfs -rm /user/hadoop/problem1-results-count/*
--sh hdfs dfs -rmdir /user/hadoop/problem1-results-count
------------------------------------------------------------------------
-- Don't try to store it, it just store the intermediate results, no
-- store record_count into '/user/hadoop/problem1-results-count' using PigStorage();
DUMP record_count;
-- result 1622294
------------------------------------------------------------------------
--sh hdfs dfs -ls /user/hadoop/problem1-results-group
--sh hdfs dfs -cat /user/hadoop/problem1-results-group/part-r-00049
------------------------------------------------------------------------



========================================================================
-- 2A/B - Compute a histogram on test file/chunk-0000  (changing the grouping by *** subject ***) !!!
------------------------------------------------------------------------
--raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
-- later you will load to other files, example:
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

------------------------------------------------------------------------
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
subjects_by_count = group count_by_subject by count PARALLEL 50;

--sub_counts = FOREACH subjects_by_count GENERATE count_by_subject.count;
--x =  DISTINCT sub_counts;
--DUMP x;

histogram = FOREACH subjects_by_count GENERATE group AS x, COUNT(count_by_subject) AS y; 
--DUMP histogram;
--ILLUSTRATE histogram;

histogram_all = GROUP histogram ALL;
histogram_count = FOREACH histogram_all GENERATE COUNT(histogram.x) AS total_points;
DUMP histogram_count;
-- A:(2)   - B:(319)


------------------------------------------------------------------------
--sh hdfs dfs -rm /user/hadoop/problem2A-results-histogram/*
--sh hdfs dfs -rmdir /user/hadoop/problem2A-results-histogram
------------------------------------------------------------------------
--STORE histogram INTO '/user/hadoop/problem2A-results-histogram' USING PigStorage();
-- count distinc points
--all_histogram_points = GROUP histogram ALL;
--histogram_count = FOREACH all_histogram_points GENERATE COUNT(histogram);
--DUMP histogram_count;
-- result 
------------------------------------------------------------------------
--sh hdfs dfs -ls /user/hadoop/problem2A-results-histogram
--sh hdfs dfs -cat /user/hadoop/problem2A-results-histogram/part-r-00049
------------------------------------------------------------------------






========================================================================
-- 3 - Compute a JOIN on test and chunk-0000
------------------------------------------------------------------------

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
--filtered_ntriples = FILTER ntriples BY (subject MATCHES '.*business.*');
--filtered_join = JOIN filtered_ntriples BY subject, filtered_ntriples2 BY subject2;
------------------------------------------------------------------
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
A = FILTER ntriples BY (subject MATCHES '.*rdfabout\\.com.*');
B = FOREACH A GENERATE subject AS subject2, predicate AS predicate2, object AS object2;
C = JOIN A BY object, B BY subject2;
D = DISTINCT C;
E = GROUP D ALL;
F = FOREACH E GENERATE COUNT(D);
DUMP F;

------------------------------------------------------------------------



========================================================================
-- 4 - Compute a histogram on chunk-****  (changing the grouping by *** subject ***) !!!
------------------------------------------------------------------------

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray); 
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray)  PARALLEL 50;

------------------------------------------------------------------------
subjects = group ntriples by (subject) PARALLEL 50;
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;
subjects_by_count = group count_by_subject by count PARALLEL 50;

--sub_counts = FOREACH subjects_by_count GENERATE count_by_subject.count;
--x =  DISTINCT sub_counts;
--DUMP x;

histogram = FOREACH subjects_by_count GENERATE group AS x  PARALLEL 50; 
--histogram = FOREACH subjects_by_count GENERATE group AS x, COUNT(count_by_subject) AS y  PARALLEL 50; 
--DUMP histogram;
--ILLUSTRATE histogram;

histogram_all = GROUP histogram ALL  PARALLEL 50;
histogram_count = FOREACH histogram_all GENERATE COUNT(histogram.x) AS total_points  PARALLEL 50;
DUMP histogram_count;

/*
15/12/20 00:48:41 INFO data.SchemaTupleBackend: Key [pig.schematuple] was not set... will not generate code.
15/12/20 00:48:41 INFO input.FileInputFormat: Total input paths to process : 50
16645586 [main] INFO  org.apache.pig.backend.hadoop.executionengine.util.MapRedUtil  - Total input paths to process : 50
15/12/20 00:48:41 INFO util.MapRedUtil: Total input paths to process : 50
(3982)
*/
