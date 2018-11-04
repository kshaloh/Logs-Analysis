# Analysing Server Logs

This project creates a reporting tool that prints out reports (in plain text) based on the data in the newsdata.sql database. This reporting tool is a Python program using the psycopg2 module to connect to the database and will run in the terminal.
---
This tool will answer the 3 following questions:

1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors? 

It does this by running only one SQL query for each question in the python code. Each one of these queries rely depends on some pre-created views. See below.
---
Results can be seen in `output_logs_analysis.txt`
---
**Q1:** 2 views were created to answer this question.

`create view topArticles as select distinct path, count(*) from log where path like '/article/%' group by path order by count desc;`

This view displays 2 columns: articles' paths and their counts in descending order.

`create view topArtWithSlug as select *, replace(path,'/article/', '') as slug from topArticles;`

This view displays same 2 columns as above, but removes the prefix '/article/' from the path.
---
**Q2:** 3 views were created to answer this question.

`create view authorAndTitle as select name, title from authors, articles where authors.id = articles.author;`

This view displays 2 columns: authors' names and title of articles they wrote.

`create view titleAndCount as select title, count from articles, topArtWithSlug where articles.slug = topartwithslug.slug order by count desc;`

This view displays 2 columns: titles and number of views for each title.

`create view authorAndViews as select name, count from authorAndTitle, titleAndCount where authorAndTitle.title = titleAndCount.title order by name;`

This view displays 2 columns: Authors' names and a count of how many hits each article they wrote received.
---
**Q3:** 5 views were created to answer this question.

`create view statusAndDate as select status, time::date as date from log;`

This view displays 2 columns: HTTP status code and date only (no time).

`create view dateStatOkCount as select distinct date, count(*) from statusAndDate where status = '200 OK' group by date;`

This view displays 2 columns: date and how many times server returned status '200 OK' each day.

`create view dateStatnotOkCount as select distinct date, count(*) from statusAndDate where status != '200 OK' group by date order by date;`

This view displays 2 columns: date and how many times server returned status NOT '200 OK' each day.

`create view dateBothStatCount as select dateStatOkCount.date, count_ok, count_not_ok
from dateStatOkCount, dateStatNotOkCount where dateStatOkCount.date = dateStatNotOkCount.date;`

This view displays 3 columns: date and each day with number of OK and NOT OK status.

`create view errorratio as select date, count_ok, count_not_ok, (1.0*count_not_ok / (count_not_ok + count_ok) * 100) as err_ratio from datebothstatcount;`

This view displays 4 columns: date, both counts (OK and NOT OK) and error ratio in percent.