#heroku PSQL
def PSQL_heroku_keys():
	dbname = 'd5hvdvca9jvtnv'
	port = '5432'
	user = 'tzrpppxxjqbykc'
	host = 'ec2-52-200-48-116.compute-1.amazonaws.com'
	password = 'f57231dafc9cd0b308c44847510ed0cf28f9fe79ce704236a8062186580632f1'

	PSQL_heroku_keys = {'dbname' : dbname
						, 'port' : port
						, 'user' : user
						, 'host' : host
						, 'password' : password
						}

	return PSQL_heroku_keys

