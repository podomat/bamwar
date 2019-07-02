#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import bamdb
import datetime
import sys
import random
from time import sleep
import re
import logging
import os


class bjbot:
	# 업소정보 게시판 번호
	shop_bo_table_map = {
		'OP_KANGNAM':'200010', 
		'OP_NOKANGNAM':'200020', 
		'OP_GYONGGI':'200030', 
		'OP_INCHEON':'200040', 
		'OP_CDK':'200050', 
		'OP_GJJ':'200060', 
		'ANMA':'200070', 
		'KNMA_SEOUL':'200080', 
		'KNMA_GYONGGI':'200081', 
		'KNMA_INCHEON':'200082', 
		'KNMA_CDK':'200083', 
		'KNMA_GJJ':'200084', 
		'ROOM':'200100', 
		'KISS':'200110', 
		'LIP':'200120', 
		'HUE_SEOUL':'200130', 
		'HUE_GYONGGI':'200131', 
		'HUE_INCHEON':'200132', 
		'HUE_CDK':'200133', 
		'HUE_GJJ':'200134', 
		'HANDFETI':'200140' }
		
	
	# 후기 게시판 번호
	review_bo_table_map = {
		'OP_KANGNAM':'400010', 
		'OP_NOKANGNAM':'400020', 
		'OP_GYONGGI':'400030', 
		'OP_INCHEON':'400040', 
		'OP_CDK':'400050', 
		'OP_GJJ':'400060', 
		'ANMA':'400070', 
		'KNMA_SEOUL':'400080', 
		'KNMA_GYONGGI':'400081', 
		'KNMA_INCHEON':'400082', 
		'KNMA_CDK':'400083', 
		'KNMA_GJJ':'400084', 
		'ROOM':'400100', 
		'KISS':'400110', 
		'LIP':'400120', 
		'HUE_SEOUL':'400130', 
		'HUE_GYONGGI':'400131', 
		'HUE_INCHEON':'400132', 
		'HUE_CDK':'400133', 
		'HUE_GJJ':'400134', 
		'HANDFETI':'400140' }

	comments_tada = {
		u'후기': [
			u'후기 잘봤습니다~~~!\n이렇게 좋은 후기를 보니 저도 가슴이 설레이는것 같네요 ^^',
			u'후기 잘봤습니다!\n이렇게 좋은 후기를 보니 저도 당장 예약하고 싶어지네요 ^^',
			u'후기 감사합니다.\n후기 쓰신 정성이 느껴지고 저도 한번 보러가고 싶다는 생각이 드네요 ^^',
			u'좋은 정보 감사합니다~~!\n후기가 내용이 눈에 딱딱 들어오네요 ^^',
			u'후기 잘 봤습니다!\n이런 언니랑 둘만의 뜨거운 시간 한번 가져보고 싶네요 ^^',
			u'후기 잘 봤습니다.\n참고하겠습니다 ^^',
			u'후기 잘 보고갑니다.\n이런 언니가 있었다니, 없어지기 전에 한번 봐야할텐데요. ^^;',
			u'후기 잘봤어요~~!\n다음 달림에는 이 후기를 참고하게 될것 같습니다 ^^',
			u'후기 잘보고 갑니당~~\n이렇게 또 한 명의 좋은 언니를 알게 되네요 ^^',
			u'좋은 정보군요. 메모해야겠습니다. ^^',
			u'후기 즐감했습니다~\n요즘 달림도 잘못했는데ㅜㅜ 후끈 달아오르네요 ^^',
			u'후기 잘봤습니다~! 뜨겁네요^^',
			u'후기 잘봤습니다~ 후끈하네요 ^^',
			u'후기 잘봤습니다.\n오늘 이 언니 확 땡기네요 ^^',
			u'언니 제대로 좃서는군요~\n갑자기 출근부를 체크하게 만드시네요 ^^',
			u'언니한테 저도 서비스 받아 보고 싶네요.\n꿀같은 정보 꼭 활용해 보겠습니다 ^^',
			u'언니 연애감 좋네요.\n나한테도 이렇게 해줬으면 좋겠당..',
			u'언니 보러 가고싶은데...\n그저 후기로 대리만족이네요',
			u'매니져와의 즐거운 후기 감사합니다.',
			u'후기 잘 봤습니다.\n즐달도 하시고 좋은 정보도 공유해 주셔서 감사합니다 ^^',
			u'보물같은 언냐네요. 후기 잘봤습니다.',
			u'언니 정성가득한 후기 감사합니다!! 잘봤습니다!',
			u'언니와 업소 꿀정보 감사합니다 ^^',
			u'언냐 같은 스타일은 사랑이네요. 잘봤습니다~^^',
			u'언니 매력터지네요.\n항상 이런 언니만 만날 수 있다면 좋겠습니다 ^^',
			u'언니 너무 궁금해집니다.\n저도 한번 가봐야 겠네요.',
		],
		u'후방주의': [
			u'오우~ 이건 뭐 대박이네요 ^^',
			u'오우야~ 그림좋아요~ ^^',
			u'와.. 굿입니다~ ^^',
			u'짤 굿입니다~ 항상 즐달하십셔~~ㅋㅋ',
			u'짤 굿입니다~ 잘 보았네요',
			u'이런거 너무 좋습니다. 감사~^^',
			u'오... 너무 좋은데요!',
			u'힘이 걍 불끈 솟습니더~~ ^^',
			u'흐... 탐스럽군요',
			u'흐... 잘봤습니다. 좋은 짤 감사드려용~',
			u'캬~ 정말 멋지네요!',
			u'엄지척! 예술입니다',
			u'이런 짤은 저장이죠ㅎㅎ',
			u'오... 멋진 짤입니다~!',
			u'허어억... 이런 짤은 대체...',
			u'보기 좋네요~ ^^ 오늘도 좋은 하루 되시길~',
			u'이건 봐도봐도 질리지가 않아요 ㅋㅋ',
			u'좋은짤들 잘보고갑니다!',
			u'좋은 사진 감사히보고갑니다', 
			u'후끈해지는 짤이군여~ ㅎㅎ', 
			u'아주 바람직한 짤이네요~ ㅎㅎ',
			u'오오... 므흣므흣 하네요 ㅎㅎ',
			u'탐스러운 사진 감사합니다~',
		],
		u'이벤트': [
			u'좋은 이벤트 자주 부탁드려요~',
			u'성업하시고 대박나세요~',
			u'쭉 발전하시기 바랍니다',
			u'오늘도 건승하십시오',
			u'오늘도 대박 터뜨리세요',
			u'오늘도 성업하시고 좋은 하루 되세요',
			u'오늘도 성업하십시오'
		],
		u'동영상': [
			u'재밌네요 ^^ 잘봤습니다.',
			u'흠... 이런것도 있군요. 잘봤습니다.^^',
			u'일단 우선 잘 보겠습니다 ^^;',
			u'ㅋㅋㅋ 대단합니다. 잘보았네용~',
			u'잘봤습니다. 항상 감사합니다~',
			u'잘봤습니다. 흥미로운 것들 또 부탁드립니당~',
		],
		u'움짤': [
			u'이런 짤은 그냥 저장가야겠네요',
			u'오호... 멋진 짤입니다~!',
			u'아이고 이런... 대단하다',
			u'허어억... 이런 짤은 대체...',
			u'보기 좋네요~ ^^ 오늘도 좋은 하루 되시길~',
		],
		u'후기홍보': [
			u'후기 감사합니다. 잘보겠습니다!',
			u'즐달이시겠지요~ \n후기 잘 보겠습니다!',
			u'재밌을것 같네요!\n후기 잘 보겠습니다~',
			u'후기 잘보겠습니다.\n항상 좋은 후기 감사드려용~',
			u'후기 링크 타고 슝~ ^^',
			u'좋은 정보 잘 얻어가겠습니다 ^^',
			u'그럼 저는 바로 후기 보러!',
			u'현기증 나네요. 바로 후기보러 갑니당~',
			u'당장 보러갑니다 ㅎㅎ',
			u'잘보고오겠습니다 ^^',
			u'후기 잘 보겠습니다 ^^',
			u'어서 보러가겠습니다~',
			u'관심 가던곳인데 잘보겠습니다~',
			u'후기잘봤습니다~ 엄지척!',
			u'바로 보러가야겠네요 ㄷㄷ',
			u'잘볼게용~!',
			u'후기 잘보고가겠습니다~ ㅎㅎㅎ 즐달도 축하드립니다',
		],
	}
	

	crawling_period_days = 60
	comment_period_days = 30
	
	comment_limit_alert = u'이 게시판은 1일에 30번만 코멘트 작성이 가능합니다.'
	too_fast_comment_alert = u'너무 빠른 시간내에 게시물을 연속해서 올릴 수 없습니다.'
	freeboard_too_old_alert = u'작성한지 7일이 지난 게시물에는 코멘트를 작성할 수 없습니다!!.'
	same_comment_alert = u'동일한 내용을 연속해서 등록할 수 없습니다..'
	freeboard_comment_limit_alert = u'이 게시판은 1일에 150번만 코멘트 작성이 가능합니다.'
	page_loading_alert = u'존재하지 않는 게시판입니다.'
	
	freeboard_bo_table = '300030'
	# freeboard_target_category = [u'후방주의', u'이벤트', u'후기홍보', u'동영상', u'움짤'] # <bj맛>
	freeboard_target_category = [u'후방주의', u'이벤트', u'후기홍보'] # <휴피안>
		
	
	# 생성자
	def __init__(self, command, user_id):
		if (user_id == 'nobody'):
			self.bj_id = user_id
			self.bj_pw = 'nopw9'
			self.bj_name = u'타다'
			self.comments = bjbot.comments_tada
		else:
			self.bj_id = 'nobody'
			self.bj_pw = 'nopw9'
			self.bj_name = u'타다'
			self.comments = bjbot.comments_tada
			
		self.init_log(command)
		self.webdriver_path = '..\chromedriver\chromedriver'
		self.driver = None
			
		self.bj_url_prefix = 'http://www.clubttt.net'
		#self.bj_url_prefix = 'http://www.bamwar15.net'
		#self.bj_url_prefix = 'http://www.bamwar31.com'
		self.comment_alert = u''
		self.page_loading_timeout_sec = 90
		
	
	# 소멸자
	def __del__(self):
		if(self.driver != None):
			self.driver.close()
		self.close_log()
		
	
	# 로그 초기화
	def init_log(self, log_name):
		print('INIT-LOG: {0}'.format(log_name))
		self.log = logging.getLogger(log_name)
		self.log.setLevel(logging.INFO)
		formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(message)s', '%H:%M:%S')
		
		ch = logging.StreamHandler(sys.stdout)
		ch.setFormatter(formatter)
		self.log.addHandler(ch)
		
		if not (os.path.isdir('logs')):
			os.makedirs(os.path.join('logs'))
		
		fh = logging.FileHandler('logs/{0}.log'.format(log_name), encoding = "UTF-8")
		fh.setFormatter(formatter)
		self.log.addHandler(fh)
		
		self.log.info('START LOG, <' + self.bj_name + '>')
		
		
	# 로그 close
	def close_log(self):
		for handler in self.log.handlers:
			handler.close()
			self.log.removeFilter(handler)
		
	
	# 웹 드라이버 초기화
	def init_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('log-level=1')
		options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images":2})
		self.driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
		self.driver.implicitly_wait(5)
		self.driver.set_page_load_timeout(self.page_loading_timeout_sec)
		
		
	# 로그인
	def login(self):
		login_url = self.bj_url_prefix + '/bbs/login.php'
		id_elem_id = 'txt_userid'
		pw_elem_id = 'txt_userpw'
		login_button_xpath = '//*[@id="btn_login"]/img'
		
		self.driver.get(login_url)
		self.driver.find_element_by_id(id_elem_id).send_keys(self.bj_id)
		self.driver.find_element_by_id(pw_elem_id).send_keys(self.bj_pw)
		self.driver.find_element_by_xpath(login_button_xpath).click()
		
	
	# 리셋
	def reset(self):
		self.driver.close()
		self.init_driver()
		self.login()
		
		
	# 쿼리 스트링에서 특정 attribute 의 value 리턴
	def get_qrystr_attr_val(self, url, attr):
		attr = attr + '='
		begin = url.find(attr)+len(attr)
		end = url[begin:].find('&')+begin # attribute가 url의 마지막에 있는 경우는 고려 안함
		return url[begin:end]

	
	# 게시물 목록에서 지정된 게시물의 등록일 추출
	def get_regidate(self, soup):
		#self.log.info(soup)
		regidate = soup.find_all('td')[5].string
		return regidate
		
	
	# 게시물 내에서 등록일시 추출
	def get_regitime(self, soup):
		info = soup.find('div', {'class':'info'})
		if (info == None):
			return None
		info = soup.find('div', {'class':'info'}).get_text().strip().replace('\t','').replace('\n','').replace('|','').split(' ')
		regitime = info[3] + ' ' + info[5]
		return regitime
		
		
	# 게시물 목록에서 지정된 게시물의 번호 추출
	def get_post_num(self, soup):
		num = soup.find('td').string
		return num
		
		
	# 게시물 페이지(url)을 열어서 등록시간, 내용 리턴
	def read_review_data(self, url):
		review_link = self.bj_url_prefix + url
		self.driver.get(review_link)
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		regitime = self.get_regitime(soup)
		if (regitime == None):
			return None
			
		content = soup.find('td', {'id':'article-content-section'}).get_text().strip()
		
		return [regitime, content]
		
		
	# 게시물 목록의 등록일('월-일' 형식)을 분석하여 일정기간 이상된 것인지(crawling 대상 인지) 판단
	def is_too_old_review(self, regidate, type):
		if (type == 'forCrawl'):
			limit_days = bjbot.crawling_period_days
		elif (type == 'forComment'):
			limit_days = bjbot.comment_period_days
		else:
			return None
	
		if(regidate.find(':') >= 0):
			return False
			
		tmp_dt = regidate.split('-')
		cur_dt = datetime.datetime.today()
		reg_dt = datetime.datetime.strptime('{0}-{1}-{2}'.format(cur_dt.year, tmp_dt[0], tmp_dt[1]), '%Y-%m-%d')
		if(reg_dt > cur_dt):
			reg_dt = datetime.datetime.strptime('{0}-{1}-{2}'.format(cur_dt.year-1, tmp_dt[0], tmp_dt[1]), '%Y-%m-%d')
			
		if(reg_dt < cur_dt - datetime.timedelta(days=limit_days)):
			return True
			
		return False
		
	
	# 댓글 중에 내가 작성한 댓글이 있는지 확인
	def is_there_my_comment(self, soup):
		comment_list = soup.find_all('li', {'class':'comment_row depth0'})
		
		if (len(comment_list) == 0):
			#self.log.info('There is no comment')
			return False
			
		for comment in comment_list:
			name = comment.find('div', {'class':'writer'}).get_text().strip()
			if(name == None):
				self.log.info("name is None, {0}".format(comment_list))
				return False
				
			if (name[:len(self.bj_name)] == self.bj_name) :
				#self.log.info('There is already my comment')
				return True
		
		return False
		
		
	# 게시물 페이지(link)를 열고 랜덤하게 댓글 작성.
	def write_comment(self, soup, category, name):
		#writer = soup.find('div', {'class':'article_head'}).find('span', {'class':'member'}).get_text()
		#message = u'{0}님, {1}'.format(writer, self.comments[category][random.randrange(0,len(self.comments[category])-1)])
		message = self.comments[category][random.randrange(0,len(self.comments[category])-1)]
		if (name != None):
			message = name + ' ' + message
		self.log.info('   >> [ADD Comment]: {0}'.format(message))
		
		try:
			self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#mw_basic_comment_write_form > form > table > tbody > tr > td:nth-child(1) > div.cheditor-container > div.cheditor-editarea-wrapper > iframe'))
		except Exception as e:
			print(e)
			return 100
		
		comment_box = self.driver.find_element_by_tag_name('body')
		comment_box.send_keys(message)
		self.driver.switch_to_default_content()
		#self.driver.find_element_by_xpath('//*[@id="btn_comment_submit"]').click()
		try:
			self.driver.find_element_by_id('btn_comment_submit').click()
		except TimeoutException:
			self.log.info('   >> Add Comment Timeout')
			self.reset()
			
		return 0
		
		

	# 댓글 작성시 alert 뜨는지 확인
	def is_comment_alert(self):
		try:
			alert = self.driver.switch_to_alert()
			if(alert != None):
				self.comment_alert = alert.text.strip()
				self.log.info('   >> Alert: {0}'.format(self.comment_alert))
				alert.accept()
				return True
		except NoAlertPresentException as e:
			pass
		except Exception as e:
			self.log.info('Exception: {0}'.format(e))
		
		return False
		
		
	def get_rank_for_image(self, image_url):
		ranks = {
			'/static/img/level/m/lv1.gif' : '훈련병',
			'/static/img/level/m/lv2.gif' : '1급병',
			'/static/img/level/m/lv3.gif' : '2급병',
			'/static/img/level/m/lv4.gif' : '3급병',
			'/static/img/level/m/lv5.gif' : '4급병',
			'/static/img/level/m/lv6.gif' : '5급병',
			'/static/img/level/m/lv7.gif' : '6급병',
			'/static/img/level/m/lv8.gif' : '7급병',
			'/static/img/level/m/lv9.gif' : '8급병',
			'/static/img/level/m/lv10.gif' : '9급병',
			'/static/img/level/m/lv11.gif' : '1성장교',
			'/static/img/level/m/lv12.gif' : '2성장교',
			'/static/img/level/m/lv13.gif' : '3성장교',
			'/static/img/level/m/lv14.gif' : '4성장교',
			'/static/img/level/m/lv15.gif' : '5성장교',
			'/static/img/level/m/lv16.gif' : '장군',
			'/static/img/level/m/lv17.gif' : '대장군',
			'/static/img/level/m/lv18.gif' : '사령관',
			'/img/level/m19.png' : '군의관',
			'/img/level/f19.png' : '간호장교',
			'/img/level/m20.png' : '총사령관',
			'/img/level/m21.png' : '원수',
			'/static/img/level/m/lv94.gif' : '실장'
			'/static/img/level/m/lv99.gif' : '운영자'
		}
		
		try:
			rank = ranks[image_url]
		except:
			rank = 'Unknown'
		
		return rank
	
	
	# 비밀글인지 확인
	def is_blocked(self, soup):
		info = soup.find('div', {'class':'wrap_info'})
		if(info != None):
			text = info.get_text().strip()
			if(text == '비밀번호 확인'):
				self.log.info('It is blocked')
			else:
				self.log.info(text)
			return True
		
		return False
		
	
	# 본문 중에 파트너 이름을 추출
	def get_partner_name(self, contents):
		unknown_phrase = ['모름','안물어봄','기억']
		contents = contents.replace(':\n', ':').replace(': \n', ':').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('\r', '').replace('⑥', '\n⑥').replace('<br />', '')
		p = re.compile('[+][0-9]')
		contents = p.sub('', contents)
		contents = contents.replace('+', '/')
		name = None
		contents = '\n'.join(x for x in contents.split('\xa0'))
		lines = contents.split('\n')
		for line in lines:
			if (line[:9] == '⑤ 파트너 이름:'):
				self.log.info(line)
				name = line[9:].strip()
				for phr in unknown_phrase:
					if(name.find(phr) >= 0):
						name = '이름모를 매니저'
				if (len(name) <= 0): name = None
				break
		return name
		
		
	
	# 게시물 목록의 글제목에서 카테고리 추출
	def get_category(self, soup):
		category = soup.find('a', {'class':'mw_basic_list_category'}).get_text().strip()
		category = category[1:len(category)-1]
		return category
		
		
	# 게시물 목록의 글제목에서 글쓴이 닉네임 추출
	def get_writer(self, soup):
		writer = soup.find('a', {'class':'uname usr_hp_normal'}).get_text().strip()
		return writer
		
		
	# 게시물 목록에서 종족 표시가 있는지 확인
	def is_brood_mark(self, soup):
		brood = soup.find_all('td', {'class':'etc'})[2].find('img')
		if(brood == None):
			return False
		return True
		

	# 게시물 목록에서 계급 이름 추출
	def get_rank(self, soup):
		rank_image = soup.find_all('td')[3].find('img')
		if rank_image == None: return None
		rank_image = rank_image['src'].split('?')[0]
		self.log.info('rank_image: {}'.format(rank_image))
		return self.get_rank_for_image(rank_image)
				
	
	# 지정된 후기게시판의 후기들을 차례로 열어서 자동으로 댓글을 작성
	def run_reviewboard_auto_comment(self, board, fullscan, start):
		page = 0
		completed = False
		started = True
		sequence_of_my_comment = 0
		
		self.close_log()
		self.init_log(board)
		
		if(start != None): started = False
		
		while completed == False:
			page = page + 1
			bo_table = bjbot.review_bo_table_map[board]
			reviewlist_url = self.bj_url_prefix + '/bbs/board.php?bo_table={0}&page={1}'.format(bo_table, page)
	
			retry_count = 0
			while True:
				try:
					self.driver.get(reviewlist_url)
					html = self.driver.page_source
					soup = BeautifulSoup(html, 'html.parser')

				except UnexpectedAlertPresentException as e:
					self.driver.switch_to_alert().accept()
					self.log.info('   >> Loading Error(UnexpectedAlertPresentException): {0}'.format(reviewlist_url))
					self.driver.reset()
					if (retry_count < 3):
						retry_count = retry_count + 1
						continue
				
				break
				
			if (retry_count >= 3):
				self.log.info('   >> Too many loading fail (review list)')
				break
					
			review_list = soup.find_all('tr', {'class':'post-item'})
			if(len(review_list)==0):
				self.log.info('   >> There is no review list.')
				break
			
			db = bamdb.BamDB()
			
			index = 0
			for review in review_list:
				index = index + 1
				loading_timeout = False
				
				ls = review.find('a', {'class':'link_subject'})
				if (ls == None):
					continue
					
				link = '{0}/bbs/{1}'.format(self.bj_url_prefix, ls['href'])
				wr_id = self.get_qrystr_attr_val(link, 'wr_id')
				writer = self.get_writer(review)
				rank = self.get_rank(review)
				title = ' '.join(x for x in review.find('a', {'class':'link_subject'}).get_text().strip().split('\xa0'))
				
				# 베스트글 skip
				if(self.get_post_num(review) == None):
					#self.log.info('   >> Skip this post, reason= "BEST post"')
					continue
					
				self.log.info('')
				self.log.info('')
				self.log.info(u'[TITLE]: {0} ({1},{2})'.format(title, writer, rank))
				self.log.info(u'[{0}-{1}-{2},{3}] {4}'.format(board, page, index, wr_id, link))
				
				# 시작 게시물을 지정한 경우, 시작 게시물에 도달했는지 확인
				if(started == False):
					if (wr_id <= start):
						started = True
					else:
						self.log.info('   >> Skip this post, reason= "Not yet starting point appeared", start={0}, wr_id={1}'.format(start, wr_id))
						continue
				
				# 댓글 작성이 불가한 오래된 후기를 만나면 게시판 순회 종료
				regidate = self.get_regidate(review)
				if(self.is_too_old_review(regidate, 'forComment') == True):
					self.log.info('   >> Skip this post, reason= "Too old article, regidate={0}"'.format(regidate))
					completed = True
					break
					
				# 내가 쓴 글은 댓글 skip
				if(writer == self.bj_name):
					self.log.info('   >> Skip this post, reason= "It is my post"')
					continue
				
				# 본문 페이지 로딩
				retry_count = 0
				while True:
					try:
						self.driver.get(link)
						review_page_html = self.driver.page_source
						review_page_soup = BeautifulSoup(review_page_html, 'html.parser')
						
					except UnexpectedAlertPresentException as e:
						self.log.info('   >> Loading Error(UnexpectedAlertPresentException): {0}'.format(link))
						self.log.info(e)
						self.driver.switch_to_alert().accept()
						if (retry_count < 3):
							retry_count = retry_count + 1
							continue
							
					except TimeoutException as e:
						self.log.info('   >> Loading Timeout: {0}'.format(link))
						self.log.info(e)
						loading_timeout = True
						#self.driver.execute_script("return window.stop")
						#self.reset()
						#retry_count = 3
						break
						
					#except UnexpectedAlertPresentException:
						#self.log.info('   >> Loading Error (UnexpectedAlertPresentException): {0}'.format(link))
						#self.reset()
						#continue
						
					except Exception as e:
						self.log.info('   >> Loading Error: {0}'.format(link))
						self.log.info(e)
						if (retry_count < 3):
							retry_count = retry_count + 1
							continue
					break
					
				if (retry_count >= 3):
					self.log.info('   >> Skip this post, reason= "Too many loading fail"')
					continue
					
				if (loading_timeout == True):
					continue
				
				# 비밀글인지 확인
				if(self.is_blocked(review_page_soup) == True):
					self.log.info('   >> Skip this post, reason= "Blocked post"')
					continue
				
				# 나의 댓글이 이미 존재하는지 확인해서 없는 경우만 수행
				if(self.is_there_my_comment(review_page_soup) == True):
					sequence_of_my_comment = sequence_of_my_comment + 1
					self.log.info('   >> Skip this post, reason= "There is already my comment. Sequential number: {0}"'.format(sequence_of_my_comment))
					if (fullscan == True):
						continue
					else: 
						if (sequence_of_my_comment >= 5): # 나의 댓글이 연속 5회 이상 발견되면 중단
							self.log.info('   >> Job complete (simple)')
							completed = True
							break
						else:
							continue
				else:
					sequence_of_my_comment = 0
						
				contents = review_page_soup.find('td', {'id':'article-content-section'}).get_text()
				partner_name = self.get_partner_name(contents)
					
				if(index>1):
					sleep(8)
				
				while True:
					# 댓글 작성
					self.write_comment(review_page_soup, u'후기', partner_name)
					
					# 댓글 작성 에러 처리
					if(self.is_comment_alert() == True):
						if(self.comment_alert == bjbot.comment_limit_alert):
							completed = True
						elif(self.comment_alert == bjbot.too_fast_comment_alert):
							sleep(10)
							continue
						elif(self.comment_alert == bjbot.same_comment_alert):
							sleep(12)
							continue
					break
				
				if (completed == True):
					break
					
					
	def write_comment_to_single_review(self, link):
		# 본문 페이지 로딩
		loading_timeout = False
		retry_count = 0
		while True:
			try:
				self.driver.get(link)
				review_page_html = self.driver.page_source
				review_page_soup = BeautifulSoup(review_page_html, 'html.parser')
				
			except UnexpectedAlertPresentException as e:
				self.log.info('   >> Loading Error(UnexpectedAlertPresentException): {0}'.format(link))
				self.log.info(e)
				self.driver.switch_to_alert().accept()
				if (retry_count < 3):
					retry_count = retry_count + 1
					continue
					
			except TimeoutException as e:
				self.log.info('   >> Loading Timeout: {0}'.format(link))
				self.log.info(e)
				loading_timeout = True
				#self.driver.execute_script("return window.stop")
				#self.reset()
				#retry_count = 3
				break
				
			#except UnexpectedAlertPresentException:
				#self.log.info('   >> Loading Error (UnexpectedAlertPresentException): {0}'.format(link))
				#self.reset()
				#continue
				
			except Exception as e:
				self.log.info('   >> Loading Error: {0}'.format(link))
				self.log.info(e)
				if (retry_count < 3):
					retry_count = retry_count + 1
					continue
			break
			
		if (retry_count >= 3):
			self.log.info('   >> Skip this post, reason= "Too many loading fail"')
			return
			
		if (loading_timeout == True):
			return
		
		# 비밀글인지 확인
		if(self.is_blocked(review_page_soup) == True):
			self.log.info('   >> Skip this post, reason= "Blocked post"')
			return
		
		# 나의 댓글이 이미 존재하는지 확인해서 없는 경우만 수행
		if(self.is_there_my_comment(review_page_soup) == True):
			self.log.info('   >> Skip this post, reason= "There is already my comment."')
			return
				
		contents = review_page_soup.find('td', {'id':'article-content-section'}).get_text()
		partner_name = self.get_partner_name(contents)
			
		while True:
			# 댓글 작성
			self.write_comment(review_page_soup, u'후기', partner_name)
			
			# 댓글 작성 에러 처리
			if(self.is_comment_alert() == True):
				if(self.comment_alert == bjbot.comment_limit_alert):
					completed = True
				elif(self.comment_alert == bjbot.too_fast_comment_alert):
					sleep(10)
					continue
				elif(self.comment_alert == bjbot.same_comment_alert):
					sleep(12)
					continue
			break


	# 지정된 게시판과 지역에 해당하는 업소별 후기 목록 수집
	def run_trawl(self, board, region):
		bo_table = bjbot.shop_bo_table_map[board]
		shoplist_url = self.bj_url_prefix + '/bbs/board.php?bo_table={0}&sca={1}'.format(bo_table, region)

		self.driver.get(shoplist_url)
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		shop_list = soup.find_all('td', {'class':'subject_cell'})
		category = 'OP'
		
		db = bamdb.BamDB()
		#db.delete_old_reviews()
		
		for shop in shop_list:
			name = shop.find('a', {'class':'mw_basic_list_category'}).get_text()
			#link_postfix = '/bbs/' + shop.find('a', {'class':'link_subject'})['href']
			link_postfix = shop.find('a', {'class':'link_subject'})['href']
			link_postfix = link_postfix[link_postfix.find('/bbs/'):]
			idx1 = name.find('-')
			idx2 = name.find(']')
			shop_name = name[idx1+1:idx2]
			self.log.info('')
			self.log.info('Checking... {0} {1} ({2})'.format(region, shop_name, link_postfix))
			
			db.add_shop(shop_name, category, region, link_postfix)
			shop_id = db.get_shop_id(category, region, shop_name)
			
			# get review list
			reviewlist_url = '{0}/bbs/board.php?bo_table={1}&sca=&sfl=wr_subject||ca_name&sop=and&stx={2}-{3}'.format(self.bj_url_prefix, self.review_bo_table_map[board], region, shop_name)
			#self.log.info(  '{0} {1} : {2}'.format(region, shop_name, reviewlist_url))
			self.driver.get(reviewlist_url)
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			review_list = soup.find_all('tr', {'class':'post-item'})
			
			index = 1
			for review in review_list:
				title = review.find('em').get_text()
				#review_link = '/bbs/' + review.find('a', {'class':'link_subject'})['href']
				review_link = review.find('a', {'class':'link_subject'})['href']
				review_link = review_link[review_link.find('/bbs/'):]
				self.log.info ('{0} / {1}'.format(title, review_link))
				bo_table = self.get_qrystr_attr_val(review_link, 'bo_table')
				wr_id = self.get_qrystr_attr_val(review_link, 'wr_id')
				writer = review.find('span', {'class':'member'})
				if(writer == None): 
					self.log.info('  >> No writer ({0})'.format(title))
					continue
				writer = review.find('span', {'class':'member'}).get_text()
				manager_id = db.check_manager_id(shop_id, title)
				
				#self.log.info ('{0} / {1}'.format(title, review_link))
				
				# 기존에 수집된 후기나 너무 오래된 후기인지 확인
				check = db.check_review(bo_table, wr_id)
				if(check == 'Exist' or check == 'Error' or check == 'TooOld'):
					#self.log.info('Skip review: {0}({1})'.format(wr_id, check))
					continue
				
				# 기존에 매니저 불명으로 등록된 것은 확인됐으면 매니저 정보 업데이트
				if(check == 'UnrecognizedManager'):
					#self.log.info('{0}: wr_id={1}'.format(check, wr_id))
					if(manager_id != None):
						self.log.info(' > Update manager: wr_id={0}, manager_id={1}'.format(wr_id, manager_id))
						db.update_manager_id (bo_table, wr_id, manager_id)
					continue
				
				regidate = self.get_regidate(review)
				if(self.is_too_old_review(regidate, 'forCrawl') == True):
					self.log.info(' > Too old review: wr_id={0}, date={1}'.format(wr_id, regidate))
					break
				
				review_data = self.read_review_data(review_link)
				if(review_data == None):
					self.log.info('Invalid review: {0}'.format(wr_id))
					continue
					
				posted_at = review_data[0]
				content = review_data[1]
				
				db.add_review(bo_table, wr_id, shop_id, manager_id, title, writer, posted_at, review_link, content)
				index = index + 1
				
				
	# 후기홍보글 본문에서 후기 링크 추출
	def get_review_link_in_a_ad(self, page_soup):
		link = None
		bonmun = page_soup.find('div', {'id':'article-content'})
		alist = bonmun.find_all('a')
		for a in alist:
			if (a['href'] != None):
				href = a['href']
				if (href.find('bo_table=400') > 0):
					p = href.find('board.php')
					link = self.bj_url_prefix + '/bbs/' + href[p:]
					break
		return link

				
	# 자유게시판의 글들을 차례로 열어서 자동으로 댓글을 작성
	def run_freeboard_auto_comment(self, fullscan, start, start_page):
		page = 0
		completed = False
		started = True
		last_wr_id = 0
		sequence_of_my_comment = 0
		
		self.close_log()
		self.init_log('FREEBOARD')

		
		if(start != None): 
			started = False
			last_wr_id = int(start)
			
		if (start_page != None):
			page = int(start_page) - 1

		
		while completed == False:
			page = page + 1
			list_url = self.bj_url_prefix + '/bbs/board.php?bo_table={0}&page={1}'.format(bjbot.freeboard_bo_table, page)
	
			self.driver.get(list_url)
			self.log.info('Loading... {0}'.format(list_url))
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			#article_list = soup.find_all('tr', {'class':'post-item'})
			article_list = soup.find('div', {'id':'board_list'}).find('table').find('tbody').find_all('tr')
			if(len(article_list)==0):
				break
			
			db = bamdb.BamDB()
			
			index = 0
			for article in article_list:
				index = index + 1
				
				link = '{0}/bbs/{1}'.format(self.bj_url_prefix, article.find('a', {'class':'link_subject'})['href'])
				wr_id = self.get_qrystr_attr_val(link, 'wr_id')
				category = self.get_category(article)
				writer = self.get_writer(article)
				rank = self.get_rank(article)
				title = ' '.join(x for x in article.find('a', {'class':'link_subject'}).get_text().strip().split('\xa0'))
				
				self.log.info('')
				self.log.info('')
				self.log.info(u'[TITLE]: {0} ({1},{2})'.format(title, writer, rank))
				self.log.info(u'[FREEBOARD-{0}-{1},{2}] ({3}) {4}'.format(page, index, wr_id, category, link))
				
				# 베스트글 skip
				if(self.get_post_num(article) == None):
					self.log.info('   >> Skip this post, reason= "BEST post"')
					continue
				
				# 시작 게시물을 지정한 경우, 시작 게시물에 도달했는지 확인
				if(started == False):
					if (wr_id <= start):
						started = True
					else:
						self.log.info('   >> Skip this post, reason= "Not yet starting point appeared", start={0}, wr_id={1}'.format(start, wr_id))
						continue

				# 댓글 작성이 불가한 오래된 후기를 만나면 게시판 순회 종료
				regidate = self.get_regidate(article)
				if(self.is_too_old_review(regidate, 'forComment') == True):
					self.log.info('   >> Skip this post, reason= "Too old article, regidate={0}"'.format(regidate))
					completed = True
					break
					
				# 내가 쓴 글은 댓글 skip
				if(writer == self.bj_name):
					self.log.info('   >> Skip this post, reason= "It is my post"')
					continue
				
				# 댓글 대상 카테고리 확인
				if category not in bjbot.freeboard_target_category:
					self.log.info('   >> Skip this post, reason= "Not target category", category={0}'.format(category))
					continue
				
				# 이미 체크한 게시물인지 확인 (페이지가 넘어가면서 발생)
				#self.log.info('wr_id = {0} / last_wr_id = {1}'.format(wr_id, last_wr_id))
				if (last_wr_id != 0):
					if (int(wr_id) >= last_wr_id):
						self.log.info('   >> Skip this post, reason= "Already read", wr_id={0}, last_wr_id={1}'.format(wr_id, last_wr_id))
						continue
			
				last_wr_id = int(wr_id)
				
				# 이벤트 카테고리는 업소실장이 쓴것인지 확인
				if(category == u'이벤트' or category == u'알림') :
					#if(self.is_brood_mark(article) == True):
					rank = self.get_rank(article)
					if(rank != '군의관' and rank != '간호장교'):
						self.log.info('   >> Skip this post, reason= "Not shop\'s staff"')
						continue

				# 본문 페이지를 로딩
				retry_count = 0
				while True:
					try:
						#sleep(2)
						self.driver.get(link)
						review_page_html = self.driver.page_source
						review_page_soup = BeautifulSoup(review_page_html, 'html.parser')
						
					except TimeoutException:
						self.log.info('   >> Loading Timeout: {0}'.format(link))
						self.reset()
						retry_count = -1
						break
						
					except UnexpectedAlertPresentException:
						self.log.info('   >> Loading Error (UnexpectedAlertPresentException): {0}'.format(link))
						self.driver.switch_to_alert().accept()
						#self.reset()
						continue
						
					except Exception as e:
						self.log.info('   >> Loading Error: {0}'.format(link))
						self.log.info(e)
						self.driver.close()
						self.init_driver()
						if (retry_count < 3):
							retry_count = retry_count + 1
							continue
					break
				if (retry_count >= 3):
					self.log.info('   >> Skip this post, reason= "Too many loading fail"')
					continue
				elif(retry_count < 0):
					#self.log.info('   >> Skip this post, reason= "Loading Failed"')
					continue
				
				# 비밀글인지 확인
				if(self.is_blocked(review_page_soup) == True):
					self.log.info('   >> Skip this post, reason= "Blocked post"')
					continue
				
				# 나의 댓글이 이미 존재하는지 확인해서 없는 경우만 수행
				if(self.is_there_my_comment(review_page_soup) == True):
					sequence_of_my_comment = sequence_of_my_comment + 1
					self.log.info('   >> Skip this post, reason= "There is already my comment. Sequential number: {0}"'.format(sequence_of_my_comment))
					if (fullscan == True):
						continue
					else: 
						if (sequence_of_my_comment >= 5): # 나의 댓글이 연속 5회 이상 발견되면 중단
							self.log.info('   >> Job complete (simple)')
							completed = True
							break
						else:
							continue
				else:
					sequence_of_my_comment = 0

				# 후방주의 게시글에 이미지가 없으면 skip
				if(category == u'후방주의'):
					bonmun = review_page_soup.find('div', {'id':'article-content'})
					#self.log.info(bonmun)
					img_list = bonmun.find_all('img')
					if len(img_list) == 0:
						self.log.info('   >> Skip this post, reason= "There is no images"')
						continue
					self.log.info('   >> There is at least one image"')
						
				if(index>1):
					sleep(8)
				
				while True:
					# 댓글 작성
					self.write_comment(review_page_soup, category, None)
					
					# 댓글 작성 에러 처리
					if(self.is_comment_alert() == True):
						if(self.comment_alert == bjbot.comment_limit_alert):
							completed = True
						elif(self.comment_alert == bjbot.freeboard_comment_limit_alert):
							completed = True
						elif(self.comment_alert == bjbot.freeboard_too_old_alert):
							completed = True
						elif(self.comment_alert == bjbot.too_fast_comment_alert):
							sleep(10)
							continue
						elif(self.comment_alert == bjbot.same_comment_alert):
							sleep(12)
							continue
					break
				
				if(category == u'후기홍보') :
					review_link = self.get_review_link_in_a_ad(review_page_soup)
					if(review_link == None): self.log.info('   후기 link 추출 실패')
					else: 
						self.log.info('   후기 link: ' + review_link)				
						sleep(8)
						self.write_comment_to_single_review(review_link)
					
				if (completed == True):
					break

					
					
	def run_all_review_auto_comment(self, fullscan, start):
		reviewBoard = [
			'OP_KANGNAM', 
			'OP_NOKANGNAM', 
			'OP_GYONGGI', 
			'OP_INCHEON', 
			'OP_CDK', 
			'OP_GJJ',
			'ANMA',
			'KNMA_SEOUL',
			'KNMA_GYONGGI',
			'KNMA_INCHEON',
			'KNMA_CDK',
			'KNMA_GJJ',
			'ROOM',
			'HUE_SEOUL',
			'HUE_GYONGGI',
			'HUE_INCHEON',
			'HUE_CDK',
			'HUE_GJJ',
			'KISS',
			'LIP',
			'HANDFETI'
			]
		
		index = 0
		for board in reviewBoard :
			index = index + 1
			if(index == 1): 
				self.log.info('')
				self.log.info('Target board list:')
			self.log.info('[{0:02d}] {1}'.format(index, board))
		
		for board in reviewBoard :
			self.run_reviewboard_auto_comment(board, fullscan, start)
			start = None
			
		self.log.info('   >> All review board auto-comment job finished.')
		
		
	def add_comment_to_all_shop(self):
	
		shop_bo_table_map = {
		'200010', 
		'200020', 
		'200030', 
		'200040', 
		'200050', 
		'200060', 
		'200070', 
		'200080', 
		'200081', 
		'200082', 
		'200083', 
		'200084', 
		'200100', 
		'200110', 
		'200120', 
		'200130', 
		'200131', 
		'200132', 
		'200133', 
		'200134', 
		'200140' }
		
		for board in shop_bo_table_map:
			link = self.bj_url_prefix + '/bbs/board.php?bo_table=' + board
			print (link)
		

		
	# 파트너 이름 추출 시험용 
	'''
	def test_get_partner_name(self, url):
		self.log.info('Getting URL : {0}'.format(url))
		self.driver.get(url)
		self.log.info('Gotten URL : {0}'.format(url))
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		contents = soup.find('td', {'id':'article-content-section'}).get_text()
		
		pname = self.get_partner_name(contents)
		
		if(pname == None): self.log.info('Name is None') #self.log.info('Name is None')
		else: self.log.info(pname) #self.log.info(pname)
	'''
		
	# 후기 링크 추출 시험용 
	def test_get_partner_name(self, url):
		url = self.bj_url_prefix + url
		#self.log.info('Getting URL : {0}'.format(url))
		self.driver.get(url)
		#self.log.info('Gotten URL : {0}'.format(url))
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		link = self.get_review_link_in_a_ad(soup)
		
		if(link == None): self.log.info('추출 실패')
		else: self.log.info('추출 완료: ' + link)
		
		
	# 후기 링크 추출 시험용 
	def test(self):
		page = 0
		completed = False
		started = True
		last_wr_id = 0
		
		self.close_log()
		self.init_log('FREEBOARD')

		
		while completed == False:
			page = page + 1
			list_url = self.bj_url_prefix + '/bbs/board.php?bo_table={0}&page={1}&sca=후기홍보'.format(bjbot.freeboard_bo_table, page)
	
			self.driver.get(list_url)
			self.log.info('Loading... {0}'.format(list_url))
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			article_list = soup.find_all('tr', {'class':'post-item'})
			if(len(article_list)==0):
				break
			
			db = bamdb.BamDB()
			
			index = 0
			for article in article_list:
				index = index + 1
				
				link = '{0}/bbs/{1}'.format(self.bj_url_prefix, article.find('a', {'class':'link_subject'})['href'])
				wr_id = self.get_qrystr_attr_val(link, 'wr_id')
				category = self.get_category(article)
				writer = self.get_writer(article)
				rank = self.get_rank(article)
				title = ' '.join(x for x in article.find('a', {'class':'link_subject'}).get_text().strip().split('\xa0'))
				
				self.log.info('')
				self.log.info('')
				self.log.info(u'[TITLE]: {0} ({1},{2})'.format(title, writer, rank))
				self.log.info(u'[FREEBOARD-{0}-{1},{2}] ({3}) {4}'.format(page, index, wr_id, category, link))
				
				# 베스트글 skip
				if(self.get_post_num(article) == None):
					self.log.info('   >> Skip this post, reason= "BEST post"')
					continue
				
				# 댓글 작성이 불가한 오래된 후기를 만나면 게시판 순회 종료
				regidate = self.get_regidate(article)
				if(self.is_too_old_review(regidate, 'forComment') == True):
					self.log.info('   >> Skip this post, reason= "Too old article, regidate={0}"'.format(regidate))
					completed = True
					break
					
				# 내가 쓴 글은 댓글 skip
				if(writer == self.bj_name):
					self.log.info('   >> Skip this post, reason= "It is my post"')
					continue
				
				# 이미 체크한 게시물인지 확인 (페이지가 넘어가면서 발생)
				#self.log.info('wr_id = {0} / last_wr_id = {1}'.format(wr_id, last_wr_id))
				if (last_wr_id != 0):
					if (int(wr_id) >= last_wr_id):
						self.log.info('   >> Skip this post, reason= "Already read", wr_id={0}, last_wr_id={1}'.format(wr_id, last_wr_id))
						continue
			
				last_wr_id = int(wr_id)
				
				# 본문 페이지를 로딩
				retry_count = 0
				while True:
					try:
						#sleep(2)
						self.driver.get(link)
						review_page_html = self.driver.page_source
						review_page_soup = BeautifulSoup(review_page_html, 'html.parser')
						
					except TimeoutException:
						self.log.info('   >> Loading Timeout: {0}'.format(link))
						self.reset()
						retry_count = -1
						break
						
					except UnexpectedAlertPresentException:
						self.log.info('   >> Loading Error (UnexpectedAlertPresentException): {0}'.format(link))
						self.reset()
						continue
						
					except Exception as e:
						self.log.info('   >> Loading Error: {0}'.format(link))
						self.log.info(e)
						self.driver.close()
						self.init_driver()
						if (retry_count < 3):
							retry_count = retry_count + 1
							continue
					break
				if (retry_count >= 3):
					self.log.info('   >> Skip this post, reason= "Too many loading fail"')
					continue
				elif(retry_count < 0):
					#self.log.info('   >> Skip this post, reason= "Loading Failed"')
					continue
				
				# 비밀글인지 확인
				if(self.is_blocked(review_page_soup) == True):
					self.log.info('   >> Skip this post, reason= "Blocked post"')
					continue
					
				link = self.get_review_link_in_a_ad(review_page_soup)
				if(link == None): self.log.info('추출 실패')
				else: 
					self.log.info('추출 완료: ' + link)				
					self.write_comment_to_single_review(link)

				
				if (completed == True):
					break