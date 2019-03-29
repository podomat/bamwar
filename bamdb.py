#-*- coding: utf-8 -*-

import MySQLdb
import datetime

class DBManager : 
	__dbconn__ = None

	def __init__(self, username, userpw, dbname):
		self.__dbname__ = dbname
		self.__username__ = username
		self.__userpw__ = username

		if DBManager.__dbconn__ == None:
			DBManager.__dbconn__ = MySQLdb.connect('localhost', self.__username__, self.__userpw__, self.__dbname__, charset='utf8', use_unicode=True)
		
		self.cursor = DBManager.__dbconn__.cursor()
		self.cursor.execute('set names utf8')


	def sqlexec(self, sql):
		try:
			self.cursor = DBManager.__dbconn__.cursor()
			
			self.cursor.execute('set names utf8')
			self.cursor.execute(sql.encode('utf-8'))

			if (sql[0:5].lower() != 'select'):
				DBManager.__dbconn__.commit()
			return self.cursor
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			print(sql)
			print(e)


	def fetchone(self):
		return self.cursor.fetchone()
		
	def getconn(self):
		return DBManager.__dbconn__
		
	def getcursor(self):
		return self.cursor

	def close(self):
		if DBManager.__dbconn__ != None:
			DBManager.__dbconn__.close()


class BamDB :
	__dbname__ = 'pupa'
	__username__ = 'jykim'
	__userpw__ = 'jykim'
	
	def __init__(self):
		self.dbm = DBManager(BamDB.__username__, BamDB.__userpw__, BamDB.__dbname__)

	def show_tables(self):
		self.dbm.sqlexec('show tables')
		while True:
			data = self.dbm.fetchone()
			if data == None:
				break
			print(data[0])
		self.dbm.close()
		
	def get_shop_id(self, category, region, name):
		sql = u'select id from shops where category = \'{0}\' and region = \'{1}\' and name = \'{2}\''.format(category, region, name)
		self.dbm.sqlexec(sql)
		data = self.dbm.fetchone()
		return data[0]
	
	def check_manager_id(self, shop_id, title):
		sql = u'select name, id from managers where shop_id = {0}'.format(shop_id)
		conn = self.dbm.getconn()
		
		try:
			cursor = conn.cursor()
			cursor.execute('set names utf8')
			cursor.execute(sql.encode('utf-8'))
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			print(e)
			
		data = cursor.fetchone()
		while data is not None:
			if ( title.find(data[0]) != -1 ):
				return data[1]
			data = cursor.fetchone()

		return None
	
	def add_shop(self, shopname, category, region, link_postfix):
		sql = u'INSERT INTO shops (name, category, region, link_postfix) VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\') \
			ON DUPLICATE KEY UPDATE link_postfix = \'{3}\''.format(shopname, category, region, link_postfix)
		#print(sql)
		self.dbm.sqlexec(sql)

	
	def add_review(self, bo_table, wr_id, shop_id, manager_id, title, writer, posted_at, link_postfix, content):
		if (manager_id == None):
			manager_id = 'null'
		
		title = title.replace("'","\\'")
		content = content.replace("'","\\'")
		
		print(' > Add review: {0} shop={1} manager={2} {3}, {4}, {5}'.format(wr_id, shop_id, manager_id, title, writer, posted_at))
			
		sql = u'insert into reviews (bo_table, wr_id, shop_id, manager_id, title, writer, posted_at, link_postfix, content) \
				values ({0}, {1}, {2}, {3}, \'{4}\', \'{5}\', str_to_date(\'{6}\', \'%Y-%m-%d %H:%i\'), \'{7}\', \'{8}\')'.format(
				bo_table, wr_id, shop_id, manager_id, title, writer, posted_at, link_postfix, content)

		try:
			conn = self.dbm.getconn()
			cursor = self.dbm.getcursor()
			cursor.execute(sql.encode('utf-8'))
			conn.commit()
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			if (e.args[0] == 1062):
				sql = u'update reviews set posted_at = str_to_date(\'{0}\', \'%Y-%m-%d %H:%i\'), content = \'{1}\' where bo_table = {2} and wr_id = {3}'.format(posted_at, content, bo_table, wr_id)
				cursor.execute(sql.encode('utf-8'))
				conn.commit()
			else:
				print(e)
					
		
	def check_review(self, bo_table, wr_id):
		TOO_OLD_PERIOD_DAYS = 30
	
		#sql = u'select count(*) from reviews where bo_table = {0} and wr_id = {1}'.format(bo_table, wr_id)
		sql = u'select posted_at, manager_id from reviews where bo_table = {0} and wr_id = {1}'.format(bo_table, wr_id)
		try:
			cursor = self.dbm.getcursor()
			cursor.execute(sql.encode('utf-8'))
			data = cursor.fetchone()
			if(data == None):
				#print('[check_review] data is None: {0}'.format(wr_id))
				return 'NotExist'

			if (data[0] == None):
				print('[check_review] data[0] is None: {0}'.format(wr_id))
				return 'NotExist'

			'''
			posted_at = data[0] # MariaDB의 datetime 타입은 변환없이 바로 python의 datetime 클래스로 받아진다.
			if (posted_at < datetime.datetime.now() - datetime.timedelta(days=TOO_OLD_PERIOD_DAYS)):
				return 'TooOld'
			'''
				
			manager_id = data[1]
			if (manager_id == None):
				return 'UnrecognizedManager'
				
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			print(e)
			return 'Error'
		
		#return (int(data[0])>0)
		return 'Exist'
		
	def update_manager_id(self, bo_table, wr_id, manager_id):
		sql = u'UPDATE reviews SET manager_id = {0} WHERE bo_table = {1} AND wr_id = {2}'.format(manager_id, bo_table, wr_id)
		self.dbm.sqlexec(sql)
		
	
	def add_regular_event_shop(self, name, region, category, option, cost_coupon, free_coupon):
		sql = u'INSERT INTO re_shops (name, region, category, option, cost_coupon, free_coupon) VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},{5}) \
			ON DUPLICATE KEY UPDATE cost_coupon = {4}, free_coupon = {5}'.format(name, region, category, option, cost_coupon, free_coupon)
		self.dbm.sqlexec(sql)
		
		
	def get_regular_event_shop_id(self, name):
		sql = u'SELECT id FROM re_shops where name = \'{0}\''.format(name)
		self.dbm.sqlexec(sql)
		data = self.dbm.fetchone()
		if(data == None): return None
		return data[0]
		
	def add_regular_event_applicant(self, id, nickname, rank, choice1_name, choice2_name, choice3_name):
		choice1_id = self.get_regular_event_shop_id(choice1_name)
		if(choice1_id == None) : 
			choice1_id = 0
		else:
			sql = u'UPDATE re_shops SET choice1 = choice1 + 1 WHERE id = {0}'.format(choice1_id)
			self.dbm.sqlexec(sql)
		choice2_id = self.get_regular_event_shop_id(choice2_name)
		if(choice2_id == None) : 
			choice2_id = 0
		else:
			sql = u'UPDATE re_shops SET choice2 = choice2 + 1 WHERE id = {0}'.format(choice2_id)
			self.dbm.sqlexec(sql)
		choice3_id = self.get_regular_event_shop_id(choice3_name)
		if(choice3_id == None) : 
			choice3_id = 0
		else:
			sql = u'UPDATE re_shops SET choice3 = choice3 + 1 WHERE id = {0}'.format(choice3_id)
			self.dbm.sqlexec(sql)
		
		sql = u'INSERT INTO re_applicants (user_id, nickname, choice1_id, choice2_id, choice3_id, choice1_name, choice2_name, choice3_name, rank) \
			VALUES (\'{0}\',\'{1}\',{2},{3},{4},\'{5}\',\'{6}\',\'{7}\',\'{8}\') \
			ON DUPLICATE KEY UPDATE choice1_id = {2}, choice2_id = {3}, choice3_id = {4}, choice1_name = \'{5}\', choice2_name = \'{6}\', choice3_name = \'{7}\''.format(
			id, nickname, choice1_id, choice2_id, choice3_id, choice1_name, choice2_name, choice3_name, rank)
		self.dbm.sqlexec(sql)
		
	def init_regular_event_table(self):
		sql = u'DELETE FROM re_applicants'
		self.dbm.sqlexec(sql)
		sql = u'ALTER TABLE re_applicants AUTO_INCREMENT = 1'
		self.dbm.sqlexec(sql)
		
		sql = u'DELETE FROM re_shops'
		self.dbm.sqlexec(sql)
		sql = u'ALTER TABLE re_shops AUTO_INCREMENT = 1'
		self.dbm.sqlexec(sql)
		
		
		
	def insert_user_statistics(self, user_id, month, fb_post_num, rb_post_num, eb_post_num, like_num, dislike_num, fb_comt_num, rb_comt_num, eb_comt_num):
		sql = u'INSERT INTO user_statistics (user_id, month, fb_post_num, rb_post_num, eb_post_num, like_num, dislike_num, fb_comt_num, rb_comt_num, eb_comt_num) \
			VALUES (\'{0}\',{1},{2},{3},{4},{5},{6},{7},{8},{9}) \
			ON DUPLICATE KEY UPDATE fb_post_num={2}, rb_post_num={3}, eb_post_num={4}, like_num={5}, dislike_num={6}, fb_comt_num={7}, rb_comt_num={8}, eb_comt_num={9}'.format(
			user_id, month, fb_post_num, rb_post_num, eb_post_num, like_num, dislike_num, fb_comt_num, rb_comt_num, eb_comt_num)
		self.dbm.sqlexec(sql)
		
		
		
	def is_exist_user_stat(self, user_id, month):
		sql = u'SELECT user_id FROM user_statistics where user_id=\'{0}\' and month={1}'.format(user_id, month)
		self.dbm.sqlexec(sql)
		data = self.dbm.fetchone()
		if(data == None): return False
		return True
		
		
	def insert_winner_info(self, id, category, shop, type, month, event):
		sql = u'INSERT INTO coupon_winning (user_id, category, shop, type, month, event) VALUES \
			(\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},\'{5}\')'.format(id, category, shop, type, month, event)
		self.dbm.sqlexec(sql)
		
		
	def insert_applications(self, user_id, month, event, shop, ordering):
		sql = u'INSERT INTO applications (user_id, month, event, shop, ordering) VALUES \
			(\'{0}\',{1},\'{2}\',\'{3}\',{4})'.format(user_id, month, event, shop, ordering)
		self.dbm.sqlexec(sql)
		
		
	def delete_applications(self, month, event):
		sql = u'DELETE FROM applications WHERE event = \'{0}\' and month={1}'.format(event, month)
		self.dbm.sqlexec(sql)
		
		
	def get_re_applicant_list(self):
		ui_list = []
		sql = u'select user_id, nickname, choice1_name, choice2_name, choice3_name, point from user_info order by point desc'
		self.dbm.sqlexec(sql)
		while True:
			ui = self.dbm.fetchone()
			if (ui != None):
				ui_list.append(ui)
			else:
				break
		return ui_list
		
		
	def get_re_coupon_winning(self, user_id, month):
		sql = u"select concat(shop, '/', type) from coupon_winning where user_id = \'{0}\' and month = {1}".format(user_id, month)
		self.dbm.sqlexec(sql)
		data = self.dbm.fetchone()
		if(data == None): return '----------'
		return data[0]

				
	def get_re_shop_list(self):
		si_list = []
		sql = u'select name, free_coupon, cost_coupon from re_shops'
		self.dbm.sqlexec(sql)
		while True:
			si = self.dbm.fetchone()
			if (si != None):
				si_list.append(si)
			else:
				break
		return si_list
	
	'''
	def get_new_review(self, period):
		sql = u'select * from reviews where read_yn = \'N\' and posted_at > now() - interval {0} day'.format(period)
		try:
			cursor = self.dbm.getcursor()
			cursor.execute(sql.encode('utf-8'))
			data = cursor.fetchone()
	'''
	

if __name__ == '__main__':
	db = BamDB()
