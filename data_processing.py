"""
  数据处理的通用类
"""
import requests
import datetime
import time
from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker

# 创建&返回session
def get_db_session():
	# 需要改成自己的数据库配置
	engine = create_engine('mysql+mysqlconnector://xxx:xxx@xxx:3306/car_data')
	# 创建DBSession类型:
	DBSession = sessionmaker(bind=engine)
	# 创建session对象:
	session = DBSession()
	sql_stmt = "SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'"
	session.execute(sql_stmt)

	return engine, session

# 获取要抓取的汽车列表
def get_car_list(session):
	sql_stmt = 'SELECT `id`, name, pic_url FROM car_basic'
	items = session.execute(sql_stmt)

	car_list = []
	for item in items:
		temp = {}
		temp = {'id': item[0], 'name': item[1], 'pic_url': item[2]}
		car_list.append(temp)
	return car_list

# 得到idataapi的API Key
def get_api_key():
	return 'xxx'

def get_html_text(url):
	for i in range(5):
		try:
			res = requests.get(url,timeout = 30)
			res.raise_for_status()
			res.encoding = res.apparent_encoding
			return res.text
		except:
			print('发现错误，等待1秒 继续重试')
			time.sleep(1)
	return "Error"

# 得到今天的日期
def get_today():
	today = datetime.date.today()
	return today

# url网址缩短，去掉?后面的
def get_short_url(url):
	try:
		index2 = url.rindex('?')
		return url[0:index2]
	except:
		return url
