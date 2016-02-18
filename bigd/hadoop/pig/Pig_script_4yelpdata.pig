-- *******   PIG LATIN SCRIPT for Yelp Assignmet ******************

-- 0. get function defined for CSV loader

register /usr/lib/pig/piggybank.jar;
register /usr/lib/pig/datafu.jar;
--register /home/cloudera/incubator-datafu/datafu-pig/build/libs/datafu-pig-incubating-1.3.0-SNAPSHOT.jar;
define CSVLoader org.apache.pig.piggybank.storage.CSVLoader();

-- 1 load data

Y      = LOAD '/user/cloudera/pig/3/input/yelp_data.csv' USING CSVLoader() AS(business_id:chararray,cool,date,funny,id,stars:int,text:chararray,type,useful:int,user_id,name,full_address,latitude,longitude,neighborhoods,open,review_count,state);
Y_good = FILTER Y BY (useful is not null and stars is not null);

--2 Find max useful
Y_all = GROUP Y_good ALL;
Umax  = FOREACH Y_all GENERATE MAX(Y_good.useful);
DUMP Umax

-- this shows max useful rating of 28! ...

-- 3 Now limit useful field to be <=5 and then get wtd average

Y_rate  = FOREACH Y_good GENERATE business_id,stars,(useful>5 ? 5:useful) as useful_clipped;
Y_rate2 = FOREACH Y_rate GENERATE $0..,(double) stars*(useful_clipped/5) as wtd_stars;
--Y_rate2 = FOREACH Y_rate GENERATE $0..,(stars * (double)useful_clipped)/5.0 as wtd_stars;

-- 4 Rank businesses

Y_g = GROUP Y_rate2 BY business_id;
Y_m = FOREACH Y_g
      GENERATE 
          group AS business_idgroup, 
          COUNT(Y_rate2.stars) AS num_ratings,
          AVG(Y_rate2.stars) AS avg_stars,
          AVG(Y_rate2.useful_clipped) AS avg_useful,
          AVG(Y_rate2.wtd_stars) AS avg_wtdstars;
         
Y_rnk = RANK Y_m BY avg_wtdstars;

-- write to HDFS
STORE Y_rnk INTO '/user/cloudera/pig/3/Y_rnk';

-- sort
--Y_rnk_srt = ORDER Y_rnk BY rank_Y_m DESC, avg_wtdstars DESC;
--STORE Y_rnk_srt INTO '/user/cloudera/pig/3/Y_rnk_srt';
--Y_rnk_desc = RANK Y_m BY avg_wtdstars DESC;
--DUMP Y_rnk_desc;

/* ----------------------------------------------------------------------------------------
Q2. For businesses that have more than 1 rating,find the average of weighted stars across businesses.

1. Filter Y_m to choose those business with num_ratings > 1, call the relation Y_m2

2. Use a GROUP ALL to create a bag of avg_wtdstars

3. Use the AVG function in a FOREACH statment to find AVG(Y_m2.avg_wtdstars)
*/

Y_m2 = FILTER Y_m BY num_ratings > 1;

Y_g2 = GROUP Y_m2 ALL;

Y_q2 = FOREACH Y_g2
       GENERATE 
          'business with minimmum support of 2: ' AS category, 
          AVG(Y_m2.avg_wtdstars) AS avg_wtdstars;

DUMP Y_q2;



/* -----------------------------------------------------------------------------------------
Q3. Here is another way to get the average of weighted stars across businesses.

Get the average of all wtd_stars from all businsss with number of ratings > 1, grouped together.

Strategy: First, we have to group the businesses to get a count of the number of ratings. Then we filter that set - we actually already have that in Y_m2 from Question 2 above.

Then we have to use that result to select only businesses that are in that set.

Here is Pseudo-code for one way to solve it:

Start with Y_rate2, which has wtd_stars, and Y_m2 which has the businesses with number of ratings > 1

1. Join Y_rate2 with Y_m2 using business id as the key. Do you want an inner or outer join?
a> INNER, so I can exclude all the bussines with less than 2 ratings

2. Make a GROUP ALL so the wtd_stars is in a bag

3. Use FOREACH to generate the average wtd_stars,

DUMP the relation and answer the question
*/
-- weighted stars
DESCRIBE Y_rate2;

-- grouped, averaged by business and filtered by ratings > 1
DESCRIBE Y_m2;

-- inner join filter Y_rate2 by bussines with more than 1 rating
-- each output row has a unique row from Y_rate2 and all the fields from grouped table Y_m2 (repeated)
Y_rate2m2_jnd = JOIN Y_rate2 BY business_id, Y_m2 BY business_idgroup;

-- group all the rows of the join in a big bag so we can apply AVG in a FOREACH
-- note that summarization in PIG does not work summing up the values of a column over a range of rows (like in SQL)
-- in PIG the summarization functions work summing the value of a field (column) of all the rows inside a bag
Y_g3 = GROUP Y_rate2m2_jnd ALL;
DESCRIBE Y_g3;

-- this time we calculate average of the detail value (instead of the average of averages by bussines as calculated in Q2)
Y_ws3 = FOREACH Y_g3  GENERATE  Y_rate2m2_jnd.Y_rate2::wtd_stars AS wtdstars;

DESCRIBE Y_ws3;

Y_q3 = FOREACH Y_ws3  GENERATE  AVG(wtdstars.Y_rate2::wtd_stars) AS avg_wtd_stars;
     
DUMP Y_q3;

/* Notice that the average of the average-weighted-stars is not the same as the average of all weighted-stars. 
This is sometimes called simpson's paradox, or the pooling problem, 
because the averages can be misleading, in some cases.

Under what condition would you prefer to report the average of the average, or the average of all wtd_stars grouped together?

If you know that the businesses are similar, with similar customers and in similar neighborhoods, 
then grouping them all together will give you a better estimate of the overall average.

If you know that businesses are not the same, perhaps because of different demographics of their location or customers, 
then you should not group it all together and take averages of averages.

The other possibility is to report both, and depending on your context, 
you might need to report number of ratings as well, because that could be skewing a grouped average.
*/

/* Q5
The strategy in Question 3 was to get a grouping so we could get the num_rating and use the JOIN to only select the desired businesses.

However, JOINs might be expensive and there is another way to get the result in Q3 without doing a JOIN.
In fact, we might think of this as a PIG-like thing to do.
*/

-- 1. get the number rated and filter by that number
Ygf = FOREACH Y_g GENERATE COUNT(Y_rate2.stars) as num_rated, Y_rate2.wtd_stars as wtd_stars2use;
Ygf_gt1 = FILTER Ygf BY num_rated>1;

-- 2. What is the next step going to be, select the answer below that fills in the blank here:
-- instead of getting the bag wtd_stars2use and call it gt1_wtd_stars  (gt1_wtd_stars is the name of a bag)
-- we flatten the bag, and each one of the numbers inside is now called gt1_wtd_stars (gt1_wtd_stars is the name of a numeric field)
Y_next = FOREACH Ygf_gt1 GENERATE FLATTEN(wtd_stars2use)  AS gt1_wtd_stars;

-- 3. Group all records together

Yg2 = GROUP Y_next ALL;

DESCRIBE Yg2;
--Yg2: {group: chararray,Y_next: {(gt1_wtd_stars: double)}}

A2 = FOREACH Yg2 GENERATE AVG(Y_next.gt1_wtd_stars);

DUMP A2

