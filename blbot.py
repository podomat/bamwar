from bs4 import BeautifulSoup
import bjbot
import bamdb
import re
import time
import datetime
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException


class blbot(bjbot.bjbot):
	shop_bo_list = [
		'200010', # OP_KAN
		'200020', # OP_NKA
		'200030', # OP_GGI
		'200040', # OP_ICN
		'200050', # OP_CDK
		'200060', # OP_GJJ
		'200070', # ANMA
		'200080', # KM_SEO
		'200081', # KM_GGI
		'200082', # KM_ICN
		'200083', # KM_CDK
		'200084', # KM_GJJ
		'200100', # ROOM
		'200110', # KISS
		'200120', # LIP
		'200130', # HT_SEO
		'200131', # HT_GGI
		'200132', # HT_ICN
		'200133', # HT_CDK
		'200134', # HT_GJJ
	]

	
	def __init__(self, command, user_id):
		super().__init__(command, user_id)
		self.min_interval = 12
		self.prev_time = None
		self.reached_comment_limit = False
		self.fname_mined_bullet = './blag_mined_bullet-' + user_id
		self.fname_limit_comment = './blag_limit_comment-' + user_id
		self.fname_checked_shop = './blag_checked_shop-' + user_id
		self.fname_blag_list = './blag_list-' + user_id
		self.mined_bullet_list = self.read_mined_bullet()
		self.limit_comment_list = self.read_limit_comment()
		self.checked_shop_list = self.read_checked_shop()
		self.bo = ''
		self.shop_link = ''
		self.page_loading_timeout_sec = 30
		self.command = command
		self.need_to_change_comment = False
		self.not_commentable = False
		if (user_id == 'bjmat'):
			self.message_base = '잘봤습니다. 오늘도 대박나세요'
		elif (user_id == 'hupian'):
			self.message_base = '라인업 끝내주네요~ 오늘도 번창하세요'
		elif (user_id == 'clean'):
			self.message_base = '출근부 잘봤습니다! 오늘도 성업하세요'
		elif (user_id == 'inadream'):
			self.message_base = '프로필 너무 좋네요^^ 오늘도 좋은 하루되세요'
		self.found_bullet = False
		self.minimum_lucky_point = 200
		
		#self.blag_links = []
		#self.blag_messages = []
		
		
	#
	def write_line(self, fname, line):
		f = open(fname, 'a')
		f.write(line + '\n')
		f.close()
		
		
	def read_lines(self, fname):
		ls = []
		try:
			f = open(fname, 'r')
			ls = f.readlines()
			ls = [l[:-1] for l in ls]
		except Exception as e:
			self.log.info('Exception(read_lines): {0}'.format(e))
			
		return ls
		
		
	def write_mined_bullet(self):
		if (self.command != 'blags'): return
		self.write_line(self.fname_mined_bullet, self.bo)

	def write_limit_comment(self):
		if (self.command != 'blags'): return
		self.write_line(self.fname_limit_comment, self.bo)
		
	def write_checked_shop(self):
		if (self.command != 'blags'): return
		self.write_line(self.fname_checked_shop, self.shop_link)
		

	def read_mined_bullet(self):
		return self.read_lines(self.fname_mined_bullet)

	def read_limit_comment(self):
		return self.read_lines(self.fname_limit_comment)

	def read_checked_shop(self):
		return self.read_lines(self.fname_checked_shop)
		
		
	def read_blag_list(self, fname):
		code = False
		ls = []
		links = []
		messages = []
		
		try:
			f = open(fname, 'r', encoding='UTF8')
			ls = f.readlines()
			ls = [l[:-1] for l in ls]
		except Exception as e:
			self.log.info('Exception(read_blag_list): {0}'.format(e))
			
		for l in ls:
			if (len(l) == 0) : continue
			if (l[0] == '#') : continue
			if (l.find('http') == 0) :
				links.append(l[l.find('/bbs/'):])
			else:
				messages.append(l)
		code = True
			
		return code, links, messages

	
	# 댓글 작성
	def write_comment(self, comment):
		message = comment
		
		count = 0
		while True:
			count = count + 1
			self.prev_time = datetime.datetime.now()
			try:
				self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#mw_basic_comment_write_form > form > table > tbody > tr > td:nth-child(1) > div.cheditor-container > div.cheditor-editarea-wrapper > iframe'))
			except NoSuchElementException:
				self.not_commentable = True
				self.write_checked_shop()
				self.log.info('   > write_comment: NoSuchElementException')
				return (False, 'NoSuchElementException')
			except UnexpectedAlertPresentException:
				self.log.info('   > write_comment: UnexpectedAlertPresentException')
				return (False, 'UnexpectedAlertPresentException')
			except Exception as e:
				self.log.info('Exception(write_comment): {0}'.format(e))
				return (False, 'WriteCommentUnknownException')
				
			comment_box = self.driver.find_element_by_tag_name('body')

			self.log.info('   (Message): '+message)
			comment_box.send_keys(message)
			
			self.driver.switch_to_default_content()
			
			try:
				self.driver.find_element_by_id('btn_comment_submit').click()
			except TimeoutException:
				self.log.info('   > Add Comment Timeout')
				self.reset()
				return (False, 'AddCommentTimeoutException')
			
			loop = self.skip_comment_alert()
			
			if (loop == False): break
			
			if (self.need_to_change_comment == True):
				if (count % 2 == 0):
					message = message + '.'
				else:
					message = message[:-1]
				self.need_to_change_comment = False
				
		return (True, 'Success')
			
			
	# comment 작성시 발생하는 alert 창 닫기	
	def skip_comment_alert(self):
		loop = False
		alert = None
		try:
			alert = self.driver.switch_to_alert()
			if(alert != None):
				self.comment_alert = alert.text.strip()
				self.log.info('   > Alert: {0}'.format(self.comment_alert))
				alert.accept()
				if (self.comment_alert.find('이 게시판은 1일에') == 0):
					self.reached_comment_limit = True
					self.comment_alert = ''
					self.write_limit_comment()
					loop = False
				elif (self.comment_alert.find('너무 빠른 시간내에') == 0):
					time.sleep(1)
					loop = True
				elif (self.comment_alert.find('동일한 내용을 연속해서') == 0):
					self.need_to_change_comment = True
					time.sleep(10)
					loop = True
				elif (self.comment_alert.find('글이 존재하지 않습니다') == 0):
					time.sleep(1)
					loop = False
					
				return loop
			else:
				self.write_checked_shop()
		except NoAlertPresentException as e:
			self.write_checked_shop()
		except Exception as e:
			self.log.info('Exception(skip_comment_alert): {0}'.format(e))
			
		return loop

		
	# 총알 터질때까지 반복하여 댓글 작성
	def mine_bullet(self, link, message, is_mine_bullet):
		link = self.bj_url_prefix + link
		self.log.info('')
		self.log.info(' Info Page: '+link)
		if ( link in self.checked_shop_list ):
			self.log.info(' > It is already checked shop info page.')
			return
		
		self.shop_link = link
		
		count = 0
		while True:
			try:
				count = count + 1
				self.driver.get(link)
				html = self.driver.page_source
				soup = BeautifulSoup(html, 'html.parser')
				break
			except TimeoutException:
				self.log.info('   > Timeout Exception')
				if (count >= 2):
					self.reset()
					return
				continue
			except UnexpectedAlertPresentException:
				alert = self.driver.switch_to_alert()
				alert.accept()
				continue
			except Exception as e:
				self.log.info('Exception(mine_bullet): {0}'.format(e))
				self.reset()
				return
			
		if (self.is_there_my_comment(soup) == True): 
			self.log.info(' > There is already my comment.')
			self.write_checked_shop()
			return
		
		self.found_bullet = False

		retry_count = 0
		while True:
			if (self.prev_time != None):
				cur_time = datetime.datetime.now()
				time_delta = (cur_time - self.prev_time).total_seconds()
				if (time_delta < self.min_interval):
					time.sleep(self.min_interval - time_delta)
				
			retry_count = retry_count + 1
			self.log.info('')
			self.log.info('  * Retry[{0}] , Bullet[{1}]'.format(retry_count, is_mine_bullet))
			
			message = message[:-1] if (retry_count % 2 == 0) else message + '!'
			code, response = self.write_comment(message)
			if (code == False):
				if (response == 'AddCommentTimeoutException'):
					break
				elif (response == 'UnexpectedAlertPresentException'):
					break
			
			if (self.not_commentable == True):
				self.not_commentable = False
				break
			
			if (self.reached_comment_limit == True): break
			
			if (is_mine_bullet == False): break
			
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			
			try:
				comment_list = soup.find('div', {'id':'comment-list'}).find_all('li')
			except Exception as e:
				self.log.info(e)
				continue
			
			if (len(comment_list) == 0):
				continue
			
			found_my_comment = False

			for comment in comment_list:
				name = comment.find('div', {'class':'writer'}).get_text().strip()
				if(name == None):
					continue
					
				if (found_my_comment == True):
					if (name[:len(self.bj_name)] == '총알') :
						lucky_point = int(comment.find('span', {'class':'lucky-point'}).get_text().strip())
						if (lucky_point > self.minimum_lucky_point):
							self.found_bullet = True
							bullet_message = comment.find('div', {'class':'comment_content'}).get_text().strip()
						else:
							self.log.info('   > Too low lucky-point: {0}'.format(lucky_point))
							break
					else:
						break
					
				if (name[:len(self.bj_name)] == self.bj_name) :
					found_my_comment = True
					comment_id = comment['id']
		
			if (self.found_bullet == True):
				self.log.info(bullet_message)
				self.write_mined_bullet()
				break

			if (found_my_comment == True):
				css_selector = '#' + comment_id + ' > div > div.writer > a.btn_func.btn_delete'
				self.driver.find_element_by_css_selector(css_selector).click()
				alert = self.driver.switch_to_alert()
				alert.accept()
				
	
	# 업소정보 게시판 댓글 작성 및 총알 수집
	def mine_bullet_shops(self):
		index = 0
		loading_fail = False
		for bo in blbot.shop_bo_list:
			self.bo = bo
			link = self.bj_url_prefix + '/bbs/board.php?bo_table=' + bo
			self.log.info('')
			self.log.info('')
			self.log.info('List Page: '+link)

			count = 0
			while True:
				try:
					count = count + 1
					self.driver.get(link)
					break
				except TimeoutException:
					self.log.info('   > Timeout Exception')
					if (count >= 2):
						loading_fail = True
						self.reset()
						break
					continue
				except Exception as e:
					self.log.info('Exception(mine_bullet_shops): {0}'.format(e))
					loading_fail = True
					break
					
			if (loading_fail == True): continue
			
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			article_list = soup.find_all('tr', {'class':'post-item'})
			
			
			if (bo in self.limit_comment_list):
				self.log.info('> Already reached limit comments')
				continue
			
			if (bo in self.mined_bullet_list):
				is_mine_bullet = False
			else:
				is_mine_bullet = True
			
			self.reached_comment_limit = False
			self.found_bullet = False
			for article in article_list:
				index = index + 1
				shop_link = '{0}/bbs/{1}'.format(self.bj_url_prefix, article.find('a', {'class':'link_subject'})['href'])
				shop_link = shop_link[shop_link.rfind('/bbs/'):]
				#wr_id = self.get_qrystr_attr_val(shop_link, 'wr_id')
				#category = self.get_category(article)
				#writer = self.get_writer(article)
				#rank = self.get_rank(article)
				#title = ' '.join(x for x in article.find('a', {'class':'link_subject'}).get_text().strip().split('\xa0'))
				#print ('{0} / {1} / {2}'.format(title, writer, shop_link))
				
				message = self.message_base + ('!' if (index % 2 == 0) else '~')
				self.mine_bullet(shop_link, message, is_mine_bullet)
				if (self.found_bullet == True):
					is_mine_bullet = False
				if (self.reached_comment_limit == True): break
			
			if (self.reached_comment_limit != True):
				self.write_limit_comment()

	
	def mine_bullet_list(self, fname):
		success, links, messages = self.read_blag_list(fname)
		if (success == False): return
		
		#for index in range(0, len(links)):
		for index, link in enumerate(links):
			self.log.info('')
			self.log.info('')
			self.log.info('LIST[{0}] {1}'.format(index, link))
			self.log.info('  > {0}'.format(messages[index]))
			self.mine_bullet(link, messages[index], True)
