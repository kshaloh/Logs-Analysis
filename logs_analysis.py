# python 3.7
# -*- coding: utf-8 -*-

import psycopg2
# connect to the news database
db = psycopg2.connect(database="news")
# set a cursor on the database
c = db.cursor()


# returns list of top 3 articles and number of views for each.
def top_three_articles():
    '''
    Run SQL query.
    This query relies on 2 dependant views (see README).
    It returns a 2 col 3 row table with the top 3 article
    titles in 1st col and number or hits it recieved from
    the log table in descending order in the 2nd col.
    '''
    c.execute('''select title, count from articles, topartwithslug
    where articles.slug = topartwithslug.slug order by count desc limit 3;''')
    # fetch result
    output = c.fetchall()
    # return result
    return output


# returns list of authors from most to least popular
def top_authors():
	'''
	Run SQL query.
    This query relies on 3 dependant views (see README).
    It returns a 2 col 4 row table with the all the authors'
    names in 1st col and number or hits each of their articles
    recieved from the previous query table in descending order
    in the 2nd col.
    '''
	c.execute('''select name, sum(count) from authorandviews
    group by name order by sum desc;''')

	output = c.fetchall()
    
	return output


# returns list of dates with more than 1% server error status.
def errors():
	''' 
	Run SQL query.
	This query relies on 5 dependant views (see README).
	It returns a 2 col 1 row table with the dates that the
	server returned more that 1% error status codes in 1st 
	col and percent of errors in the 2nd col.
	'''
	c.execute('''select date, err_ratio from errorratio where err_ratio > 1.0;''')
    
	output = c.fetchall()
    
	return output


if __name__ == '__main__':
	print("\nMost popular three articles of all time:\n")
	for entry in top_three_articles():
		# extract article title from query result
		article_title = entry[0]
		# extract view count from query result
		view_count = entry[1]
		# gives output string with atricle title and number of views.
		print("  - \"" + article_title.title() + "\"" + " — " + 
			str(view_count) + " views")

	print("\nMost popular article authors of all time:\n")
	for entry in top_authors():
		# extract author's name from query result
		author_name = entry[0]
		# extract view count from query
		view_count = entry[1]
		# gives output string with author's name and number of views.
		print("  - " + author_name + " — " + 
			str(view_count) + " views")

	print("\nDays that had more than 1% of requests lead to errors:\n")
	for entry in errors():
		# extract date from query result
		date = entry[0]
		# extract percent error from query and rounds to 2 decimal places.
		percent = round(entry[1], 2)
		# gives output string with date and percent error.
		print("  - " + str(date.strftime('%b %d,%Y')) + " — " + 
			str(percent) + "% errors\n")

	# close connection
	db.close()