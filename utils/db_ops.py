
def query(cur, sql):
	# Queries the DB corresponding to `cursor` and `sql` string..
	cursor.execute(sql)
	return cur.fetchone()