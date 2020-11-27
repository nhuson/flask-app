# python modules
import socket


# configuration class
class Config:
	# local db
	MONGODB_LOC = "mongodb://root:006c31acbeeee2031a9dd17c59e59a6d8c731db6@cotest1.abivin.vn/vApp?authSource=admin"
	
	# beta db
	MONGODB_BETA = "mongodb://root:a9fcd54b25e7e863d72cd47c08af46e61b74b561@beta1.abivin.vn/vApp?authSource=admin"
	
	# dev db
	MONGODB_DEV = "mongodb://root:095daec22e585144bc5d8853af05ad2e15d29bf4@codev1.abivin.vn/vApp?authSource=admin"
	
	# test db
	MONGODB_TEST = "mongodb://root:006c31acbeeee2031a9dd17c59e59a6d8c731db6@cotest1.abivin.vn/vApp?authSource=admin"
	
	# production db
	MONGODB_PROD = "mongodb://root:fd4181df080cdbf84e12e870cd80e75ad142d9ea@35.198.216.32,35.198.215.151/vApp?replicaSet=rs0&authSource=admin&readPreference=secondary"
	
	# datd/cluster db/begin
	MONGODB_CLUSTER = "mongodb://root:${mongodbPassword}@${cluster}1.abivin.vn/vApp?authSource=admin"
	
	# Redis
	REDIS_URL = "redis://foobar:019eb50f3dbada176f997e3934901baebe6dcb53@redis1.abivin.vn"
	
	# db names
	DB_LOC = "vApp"
	DB_DEV = "vApp"
	DB_TEST = "vApp"
	DB_PROD = "vApp"
	DB_CLUSTER = "vApp"
	DB_BETA = "vApp"
	
	# data source to operate on (_LOC, or _DEV, or _PROD)
	DB_URL = ""
	DB_NAME = ""
	POSTGRES_URL = "postgresql+psycopg2://vaddress:vadress@123!@codev1.abivin.vn:5432/vaddress"

	NEWRELIC_KEY = "c67876cf7e5c971656bd1d9bc48830c6d1d9c5b4"
	PRIVATE_TOKEN_VADDRESS = "3702efasdd600d241e1sdsd9f4e05sda34df3ss32"
	
	JWT_SECRET = "LTaJB2W5dVZ7SFwfuJtgHwONUOsvqomSOBm5o4mKBnR0vAFxHvyJaEDEnrAg9B" + \
				 "FUX4Odcv/7m+pBXRi7b2qrM0h/9X78HWeCcUzJMOrie1mGF9pFkvR8cCDqAnt+" + \
				 "Ju+7NIgN8iQAEbSv3JWXluekq8yoqFKK8Xtw/jW90Yh6gcCSKFpacIl9eiw2lK" + \
				 "wx5HXRVc+INwSH1WAZe7gdEpeGSHowsDJ5lfWENzTYkjzIt5dH2hVVmExlWPP9" + \
				 "Xure0BQX6YYecvc0c8bu5LHJxI6LYyIQkxbfZ5Bffl6p/3fbIxIZcaHgwB6+ee" + \
				 "J1LT8CT4nr1SgB/z+3WW+yMyPJa+1FKyl1VBoz5XwVDgPeVCEgBHRsfkx5iygh" + \
				 "NjU1QJYs+JMK56G/qAO1zE9A6bvLtoXS+xJalLkYojKW8SHjJ397jJ9ledf80a" + \
				 "UYr4HKRTJ0rPKB9EbSxNChBNVDwwHHHlksnTKgsRx/Nf49KKqgDf23KAcUKCJw" + \
				 "S+lQp6qT5EK0ThOow9F5AXl0RHNqzSYkCyRW/48mCyASEDtM944SZkP0zvtMqN" + \
				 "h1ptB1QG5FWzuq1E24"
	
	METABASE_CONFIG = {
		"URL": "https://meta.abivin.vn",
		"DASHBOARDS": {
			"NUMBER_OF_ORDERS_BY_ON_TIME_STATUS": 199,
			"NUMBER_OF_TRUCK_USED": 200,
			"KPI_SCOREBOARD": 201,
		},
		"SECRET_KEY": "f09e738b2ca3afe310907a4612010a2d184d2b587a6c8a82754fb3b9fcf5f117",
	}
	
	# check if on developer's machine (not on cloud)
	def is_on_developers_machine():
		connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		connection.connect(("8.8.8.8", 80))
		lan_ip = connection.getsockname()[0]
		connection.close()
		
		# developers' machine LAN ips start with 192.168
		if lan_ip[:7] == "192.168":
			return True
		else:
			return False
