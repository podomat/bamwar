from bs4 import BeautifulSoup
import bjbot
import bamdb
import re
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException


class rebot(bjbot.bjbot):
	def __init__(self, command, user_id):
		super().__init__(command, 'nobody')
		
		self.page_loading_timeout_sec = 300
		
		self.fb_post_num = 0
		self.rb_post_num = 0
		self.eb_post_num = 0
		self.like_num = 0
		self.dislike_num = 0
		
		self.fb_comt_num = 0
		self.rb_comt_num = 0
		self.eb_comt_num = 0
		
		self.check_month = 4

	def regevt_get_comment_item(self, contents, item, mark):
		if item in contents:
			if contents[contents.index(item)+1] == mark: value = contents[contents.index(item)+2]
			else: value = contents[contents.index(item)+1]
		elif item+mark in contents:
			value = contents[contents.index(item+mark)+1]
		else:
			self.log.info(contents)
			self.log.info('(warning) No item: {0}'.format(item))
			return None
			
		return value


	def regevt_get_comment_item2(self, contents, item, mark):
		if item in contents:
			if contents[contents.index(item)+1] == mark: value1_idx = contents.index(item)+2
			else: value1_idx = contents.index(item)+1
		elif item+mark in contents:
			value1_idx = contents.index(item+mark)+1
		else:
			self.log.info('(warning) No item: {0}'.format(item))
			return None
			
		value1 = contents[value1_idx]
		if (value1_idx+1 < len(contents)): value2 = contents[value1_idx+1]
		else: return None
		if (value1_idx+2 < len(contents)): value3 = contents[value1_idx+2]
		else: value3 = ''
		
		if value2[0] == '[' :
			value3 = value2
		else :
			value1 = value1 + ' ' + value2
			
		return [value1, value3]
		
		
	def regevt_get_comment_item3(self, contents, item, mark):
		if item in contents:
			value1_idx = contents.index(item)+2
		elif item+mark in contents:
			value1_idx = contents.index(item+mark)+1
		else:
			self.log.info('(warning) No item: {0}'.format(item))
			return None
			
		value1 = contents[value1_idx]
		if (value1_idx+1 < len(contents)): value2 = contents[value1_idx+1]
		else: return None
		if (value1_idx+2 < len(contents)): value3 = contents[value1_idx+2]
		else: value3 = ''
		
		if value2[0] == '[' :
			value3 = value2
		else :
			value1 = value1 + ' ' + value2
			
		return [value1, value3]
		
	
	
	# 정기 이벤트에 코멘트로 신청한 정보 수집
	def regevt_get_comments(self, html, db):
	
		'''

<< 8월 정기이벤트 신청 양식 >>

아이디: dkwk123닉네임: 아잔 
1 . 강남 타워레코드 [오피] 2 . 종각 웬디스 [스파] 3 . 신촌 민들레영토 [안마]4. 서울, 분당, 광명 [지역]

		'''
	
		#html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		comments = soup.find_all('li', {'class':'comment_row depth0'})
		
		error_count = 0
		index = 0
		for comment in comments:
			index = index + 1
			self.log.info('')
			self.log.info('< {0} >'.format(index))
			
			contents = comment.find('textarea').get_text()
			#self.log.info(contents)
			#self.log.info(' ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----')
			
			contents = contents.replace('&nbsp;',' ').replace('&amp;','&').replace('[',' [').replace('.','. ').replace(' (','(').replace(')',') ').replace(':',': ').replace(']','] ').replace(',',' ').replace(';',' ').replace('ᆞ',' ').replace('-',' ')
			contents = contents.replace('1 :','1 .').replace('2 :','2 .').replace('3 :','3 .').replace('맥심','MAXIM').replace('매직미러풀(신세경','매직미러(예쁜신세경').replace('스폐셜K','스페셜K')
			contents = contents.replace('아이다', '아이디').replace('닉네임', ' 닉네임').replace(' 실장', '실장').replace('(오피)', ' [오피]').replace('(안마)', ' [안마]')
			contents = contents.replace('닉네님','닉네임').replace('지망:','.')
			contents = contents.replace('일산', '일산 ').replace('사당', '사당 ').replace('분당', '분당 ').replace('상봉', '상봉 ').replace('잠실', '잠실 ').replace('답십리', '답십리 ')
			contents = contents.replace('강남', '강남 ').replace('부천', '부천 ').replace('도봉', '도봉 ').replace('노원', '노원 ').replace('송탄', '송탄 ').replace('동탄', '동탄 ')
			contents = contents.replace('  ', ' ')
			contents = contents.replace('(풀싸롱)', ' [풀싸롱]').replace('예쁜 ', '예쁜').replace('부천 A ', '부천 A스파 ').replace('MC ', 'MC스파 ').replace('BMT ', 'BMT편의점 ')
			contents = contents.replace('애ᄑᆕᆯ', '애플').replace('야구장 ', '야구장(윤대표) ').replace('논현 진주', '논현진주').replace(' 대표', '대표')
			contents = contents.replace('수원 과일가게', '수원 과일과게').replace('오솔로', '오슬로').replace('분당 RM', '부천 RM').replace('시흥 MAXIM', '시흥 맥심')
			contents = contents.replace('썬웨이노래광장 ', '썬웨이노래광장(이태수대표) ').replace('17%스타킹 ', '17%스타킹(원섭대표) ').replace('지중해 ', '지중해(키티실장) ')
			contents = contents.replace('치파오 ', '치파오시즌2 ').replace('왕과비(하지원)','왕과비(하지원대표)').replace('헤라','혜라').replace('방앗간휴게텔','방앗간 [휴게텔')
			contents = contents.replace('인천 JYP','부평 JYP').replace('인천 퍼플', '부평 퍼플').replace('맨투맨 ','맨투맨안마 ').replace('1%발렌타인 ','1%발렌타인(금나라실장) ')
			contents = contents.replace('논현 진주','논현진주').replace('1프로', '1%').replace('수원 MAXIM', '수원 맥심').replace('홍대요정', '홍대 요정')
			contents = contents.replace('미러초이스 ','미러초이스(예쁜제니실장) ').replace('강남 후시딘', '선릉 후시딘').replace('부천 A ', '부천 A스파 ').replace('팡팡스파', '팡팡')
			contents = contents.replace('당산 M ', '당산 M스파 ').replace('스파르타 ', '스파르타스파 ').replace('란제리 ','란제리셔츠룸(초아실장) ').replace('강남 맛집', '강남맛집')
			contents = contents.replace('강남 씨티', '강남 CT').replace('강남 씨티', '강남 CT').replace('살아있네 ','살아있네(이연수사장) ').replace('강남 강남맛','역삼 강남맛')
			contents = contents.replace('프린스 ','프린스(김종국대표) ').replace('MAXIM걸','맥심걸').replace('구리 G ', '구리 Gspa ').replace('치파오2','치파오시즌2')
			contents = contents.replace('분덩여자','분당 여자').replace('1% 발렌타인','1%발렌타인').replace('원섭상무','원섭대표').replace('심쿵','심쿨').replace('인천 엄지척','부평 엄지척')
			contents = contents.replace('남영주','남양주').replace('남양주.','남양주').replace('강맘', '강남').replace('ct','CT').replace('꿀 ','꿀스파 ').replace('배아래 민족','배아래민족')
			
			'''
			p = re.compile('야구장.*?송혜교실장[)]')
			contents = p.sub('야구장(송혜교실장)', contents)
			'''
			p = re.compile('<p.*?>')
			contents = p.sub('\n', contents)
			p = re.compile('<span.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<div.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<font.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<strong.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<br.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<b.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<a.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<!.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('</.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('^ *')
			contents = p.sub(' ', contents)
			p = re.compile('^\n')
			contents = p.sub(' ', contents)
			contents = contents.strip()
			#self.log.info(contents)
			contents_ex = contents
			
			contents = contents.split()
			self.log.info(contents)
			
			id = self.regevt_get_comment_item(contents, '아이디', ':')
			if (id == None): 
				self.log.info('Get ID fail.')
				self.log.info(contents_ex)
				error_count = error_count + 1
				continue
			
			nickname = self.regevt_get_comment_item(contents, '닉네임', ':')
			if (nickname == None): 
				self.log.info('Get Nickname fail.')
				self.log.info(contents_ex)
				error_count = error_count + 1
				continue
			
			choice1 = self.regevt_get_comment_item2(contents, '1', '.')
			if (choice1 == None): 
				self.log.info('Get 1지망 fail.')
				self.log.info(contents_ex)
				error_count = error_count + 1
				continue
			
			choice2 = self.regevt_get_comment_item2(contents, '2', '.')
			if (choice2 == None): 
				choice2 = ["",""]
				#error_count = error_count + 1
				#continue
			
			choice3 = self.regevt_get_comment_item2(contents, '3', '.')
			if (choice3 == None): 
				choice3 = ["",""]
				#error_count = error_count + 1
				#continue

			rank_img = comment.find('div', {'class':'writer'}).find_all('img', {'width':'28'})[1]['src']
			rank = self.get_rank_for_image(rank_img)
						
			self.log.info(' - ID: {0}'.format(id))
			self.log.info(' - Nickname: {0}'.format(nickname))
			self.log.info(' - Rank    : {0}'.format(rank))
			self.log.info(' - Choice 1: {0} / {1}'.format(choice1[0], choice1[1]))
			self.log.info(' - Choice 2: {0} / {1}'.format(choice2[0], choice2[1]))
			self.log.info(' - Choice 3: {0} / {1}'.format(choice3[0], choice3[1]))
			
			# Insert applicant's information
			db.add_regular_event_applicant(id, nickname, rank, choice1[0], choice2[0], choice3[0])
			
			self.get_member_statistics(id, self.check_month)
		
		return index, error_count

		
	# 정기 이벤트 업소 정보 리스트 gethering
	def regevt_get_shops(self, url, coupon_url):
	
		self.log.info('Initiating DB ...')
		db = bamdb.BamDB()
		db.init_regular_event_table() # DB에 이전 정보 삭제

		self.driver.get(coupon_url)
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		trs = soup.find('table', {'class':'waffle'}).find('tbody').find_all('tr')
		
		index = 0
		for tr in trs:
			index = index + 1
			
			if (index < 3): continue
			
			'''
			change = tr.find_all('td')[0].get_text().strip()
			if (change == '취소'): continue
			'''
			
			name = tr.find_all('td')[0].get_text().strip()
			region = tr.find_all('td')[1].get_text().strip()
			category = tr.find_all('td')[2].get_text().strip()
			cost_coupon = tr.find_all('td')[4].get_text().strip()
			if (cost_coupon == '') : cost_coupon = 0
			free_coupon = tr.find_all('td')[5].get_text().strip()
			if (free_coupon == '') : free_coupon = 0
			option = tr.find_all('td')[3].get_text().strip()
			
			self.log.info('[{6}] {0} / {1} / {2} / {3} / {4} / {5}'.format(name, region, category, option, cost_coupon, free_coupon, index-2))
			db.add_regular_event_shop(name, region, category, option, cost_coupon, free_coupon)
		
		comment_count = 0
		error_count = 0

		url = self.bj_url_prefix + url
		self.log.info('Loading first page : {0}'.format(url))
		self.driver.get(url)
		comment_count, error_count = self.regevt_get_comments(self.driver.page_source, db)
		
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		cpages = soup.find('div', {'id':'comment-paging'}).find_all('a')
		
		page_num = 1
		for cpage in cpages:
			page_num = page_num + 1
			cpage_url = self.bj_url_prefix + cpage['href']
			self.log.info('')
			self.log.info('< page {0} : {1} >'.format(page_num, cpage_url))
			
			self.driver.get(cpage_url)
			
			page_comment_count, page_error_count = self.regevt_get_comments(self.driver.page_source, db)
			comment_count = comment_count + page_comment_count
			error_count = error_count + page_error_count
			
		self.log.info('')
		self.log.info('Total Comment : {0}'.format(comment_count))
		self.log.info('')
		self.log.info('Total Error : {0}'.format(error_count))
		
	
	# 회원별 활동량 통계 수집
	def get_member_statistics(self, user_id, month):
		db = bamdb.BamDB()
		
		if (db.is_exist_user_stat(user_id, month) == True):
			self.log.info('User ({0}) statistics already exist.'.format(user_id))
			return
		
		self.get_member_statistics_by_view(user_id, month, 'w')
		self.get_member_statistics_by_view(user_id, month, 'c')
		
		self.log.info('')
		self.log.info('User ({0}) statistics (Month {1})'.format(user_id, month))
		self.log.info('  + Post   : FreeBoard={0}, ReviewBoard={1}, EtcBoard={2}, Like={3}, Dislike={4}'.format(self.fb_post_num, self.rb_post_num, self.eb_post_num, self.like_num, self.dislike_num))
		self.log.info('  + Comment: FreeBoard={0}, ReviewBoard={1}, EtcBoard={2}'.format(self.fb_comt_num, self.rb_comt_num, self.eb_comt_num))
		self.log.info('  + Total  : Post={0}, Comment={1}'.format(self.fb_post_num+self.rb_post_num+self.eb_post_num, self.fb_comt_num+self.rb_comt_num+self.eb_comt_num))
		
		
		db.insert_user_statistics(user_id, month, self.fb_post_num, self.rb_post_num, self.eb_post_num, self.like_num, self.dislike_num, self.fb_comt_num, self.rb_comt_num, self.eb_comt_num)
		
		
	
	# 회원별 view별 활동량 통계 수집
	def get_member_statistics_by_view(self, user_id, month, view):
		completed = False
		page = 0
		started = False
		category = 'Comment'
	
		url_format = self.bj_url_prefix + '/bbs/new.php?gr_id=&view={0}&mb_id={1}&page={2}'
		
		fb_num = 0
		rb_num = 0
		eb_num = 0
		lk_num = 0
		dlk_num = 0
		
		group = ''
		board = ''
		like = ''
		dislike = ''
		nickname = ''
		date = ''

		le_count = 0
		
		
		if (view == 'w'): category = 'Post'
		
		
		while completed == False:
			page = page + 1
			link = url_format.format(view, user_id, page)
		
			self.log.info('')
			self.log.info('{0} {1} page loading : {2}'.format(category, page, link))
			try:
				self.driver.get(link)
				html = self.driver.page_source
				soup = BeautifulSoup(html, 'html.parser')
				
			except UnexpectedAlertPresentException:
				self.log.info('   >> Loading Error (UnexpectedAlertPresentException): {0}'.format(link))
				alert = self.driver.switch_to_alert()
				alert.accept()
				page = page - 1
				le_count = le_count + 1
				if le_count >= 5 :
					completed = True
				continue

			except Exception as e:
				self.log.info('   >> Loading Error: {0}'.format(link))
				self.log.info(e)
				completed = True
				continue

			trs = soup.find('form', {'name':'fnewlist'}).find('table', {'class':'tmy_infoTable'}).find('tbody').find_all('tr')
			
			for tr in trs:
				tds = tr.find_all('td')
				
				number = tds[0].get_text()
				if (number == u'게시물이 없습니다.'):
					self.log.info(' -> There is no {0}.'.format(category))
					completed = True
					break
				
				group = tds[1].get_text()
				board = tds[2].get_text()
				#like = tds[4].get_text()
				#dislike = tds[5].get_text()
				like = '0'
				dislike = '0'
				nickname = tds[6].get_text()
				date = tds[7].get_text()
				
				#self.log.info('{0} / {1} / {2} / {3} / {4} / {5}'.format(group, board, like, dislike, nickname, date))
				
				if (started == True):
					if (len(date)==0):
						break
					if (int(date[5:7]) != month):
						completed = True
						break
				
				else:
					if (date == None or date == ''): continue
					if (date[2] == ':'): continue
					
					if (int(date[5:7]) == month):
						started = True
						self.log.info (' -> starting point has found.')
					elif (int(date[5:7]) < month):
						completed = True
						break
					else:
						continue

				if (board == '자유게시판'):
					fb_num = fb_num + 1
				elif (group == '업소후기'):
					rb_num = rb_num + 1
				else:
					eb_num = eb_num + 1
					
				lk_num = lk_num + int(like)
				dlk_num = dlk_num + int(dislike)

			self.log.info(' -> FreeBoard={0}, ReviewBoard={1}, EtcBoard={2}, Nickname={3}, LastDate={4}'.format(fb_num, rb_num, eb_num, nickname, date))
		
		if (view == 'w'):
			self.fb_post_num = fb_num
			self.rb_post_num = rb_num
			self.eb_post_num = eb_num
			self.like_num = lk_num
			self.dislike_num = dlk_num
		else:
			self.fb_comt_num = fb_num
			self.rb_comt_num = rb_num
			self.eb_comt_num = eb_num
			

	# 정기 이벤트 당첨자 목록 수집
	def gethering_re_winner_info(self, link):
		self.log.info('Initiating DB ...')
		db = bamdb.BamDB()
		link = self.bj_url_prefix + link
	
		self.log.info('Loading first page : {0}'.format(link))
		self.driver.get(link)
		
		self.log.info('switch to frame 1')
		#self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#article-content-section > p:nth-of-child(147) > iframe'))
		#self.driver.switch_to_frame(self.driver.find_element_by_xpath('//*[@id="article-content-section"]/p[20]/iframe'))
		self.driver.switch_to_frame(self.driver.find_element_by_xpath('//*[@id="article-content-section"]/p[15]/iframe'))
		
		
		#self.log.info('switch to frame 2')
		#self.driver.switch_to_frame(self.driver.find_element_by_css_selector('#pageswitcher-content'))
		
		
		self.log.info('Getting page source ...')
		html = self.driver.page_source
		
		self.log.info('Getting BeautifulSoup ...')
		soup = BeautifulSoup(html, 'html.parser')
		
		self.log.info('Finding trs ...')
		tbody = soup.find('tbody')
		#print(trs)
		trs = tbody.find_all('tr')
		
		index = 0
		for tr in trs:
			index = index + 1
			if (index <= 2): continue
			
			tds = tr.find_all('td')
			
			id = tds[0].get_text()
			nickname = tds[1].get_text()
			category = tds[2].get_text()
			shop = tds[3].get_text()
			type = tds[4].get_text()
			if(type == '무료'): type = '무료권'
			else: type = '원가권'
			
			self.log.info('[{0}] {1} / {2} / {3} / {4} / {5}'.format(index-2, id, nickname, category, shop, type))
			#db.insert_winner_info(id, category, shop, type, self.check_month, '정기')
			db.insert_winner_info(id, category, shop, type, 1 if self.check_month==12 else self.check_month+1, '정기')
			
			
	def gethering_wda(self, link):
		month = 8
		event = u'우리동네안마왕part1'
	
		db = bamdb.BamDB()
		
		self.driver.get(link)
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		self.evt_get_comments_type1(html, db, month, event)
		
		cpages = soup.find('div', {'id':'comment-paging'}).find_all('a')
		
		page_num = 1
		for cpage in cpages:
			page_num = page_num + 1
			cpage_url = self.bj_url_prefix + cpage['href']
			self.log.info('')
			self.log.info('< page {0} : {1} >'.format(page_num, cpage_url))
			
			self.driver.get(cpage_url)
			html = self.driver.page_source
			
			self.evt_get_comments_type1(html, db, month, event)
		
			
			
	# 우리동네 안마왕 part1 이벤트에 코멘트로 신청한 정보 수집
	def evt_get_comments_type1(self, html, db, month, event):
	
		'''

<< 8월 우리동네 안마왕 part1 신청 양식 >>

신청 양식
아이디 : jangddong  닉네임 : 그녀와의추억
1. 강남1구역  2. 서울권1구역
후기링크 : 6~7월 본인이 잘썼다고 생각하는 후기링크~

		'''
	
		soup = BeautifulSoup(html, 'html.parser')
		comments = soup.find_all('li', {'class':'comment_row depth0'})
		
		error_count = 0
		index = 0
		
		for comment in comments:
			index = index + 1
			self.log.info('')
			self.log.info('< {0} >'.format(index))
			
			contents = comment.find('textarea').get_text()
			#self.log.info(contents)
			#self.log.info(' ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----')
			
			contents = contents.replace('&nbsp;',' ').replace('[',' [').replace('.','. ').replace(' (','(').replace(':',': ').replace(']','] ').replace('닉네임', ' 닉네임')
			p = re.compile('<p.*?>')
			contents = p.sub('\n', contents)
			p = re.compile('<span.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<div.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<strong.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<br.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<b.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<a.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<!.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('</.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('^ *')
			contents = p.sub(' ', contents)
			p = re.compile('^\n')
			contents = p.sub(' ', contents)
			contents = contents.replace('강남권','강남').replace('강남 ','강남').replace('서울 ','서울권').replace('서울권 ','서울권').replace('경기권 ','경기권').replace('경기 ','경기권')
			contents = contents.strip()
			
			contents = contents.split()
			self.log.info(contents)
			
			id = self.regevt_get_comment_item(contents, '아이디', ':')
			if (id == None): 
				error_count = error_count + 1
				continue
			
			nickname = self.regevt_get_comment_item(contents, '닉네임', ':')
			if (nickname == None): 
				error_count = error_count + 1
				continue
			
			choice1 = self.regevt_get_comment_item(contents, '1', '.')
			if (choice1 == None): 
				error_count = error_count + 1
				continue
				
			choice1 = choice1.replace('1', ' 1').replace('2', ' 2').replace('3', ' 3')
			
			choice2 = self.regevt_get_comment_item(contents, '2', '.')
			'''
			if (choice2 == None): 
				error_count = error_count + 1
				continue
			'''
			'''
			choice3 = self.regevt_get_comment_item2(contents, '3', '.')
			if (choice3 == None): 
				error_count = error_count + 1
				continue
			'''
			#print (comment)
			#rank_img = comment.find('div', {'class':'writer'}).find_all('img', {'width':'28'})[1]['src']
			rank_img = comment.find('div', {'class':'writer'}).find_all('img')
			rank_img = rank_img[len(rank_img)-1]['src']
			rank = self.get_rank_for_image(rank_img)
						
			self.log.info(' - ID: {0}'.format(id))
			self.log.info(' - Nickname: {0}'.format(nickname))
			self.log.info(' - Rank    : {0}'.format(rank))
			self.log.info(' - Choice 1: {0}'.format(choice1))
			#	def insert_applications(self, user_id, month, event, shop, ordering):

			db.insert_applications(id, month, event, choice1, 1)
			if(choice2 != None): 
				choice2 = choice2.replace('1', ' 1').replace('2', ' 2').replace('3', ' 3')
				self.log.info(' - Choice 2: {0}'.format(choice2))
				db.insert_applications(id, month, event, choice2, 2)
			
			# Insert applicant's information
			#db.add_regular_event_applicant(id, nickname, rank, choice1[0], choice2[0], choice3[0])
			
			#self.get_member_statistics(id, self.check_month)
		
		return index, error_count
		
		
		
	# 서울 오피 플랜맨 이벤트
	def gethering_soplan(self, link):
		month = 8
		event = u'서울오피플랜맨'
	
		db = bamdb.BamDB()
		
		self.driver.get(link)
		html = self.driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		self.evt_get_comments_type2(html, db, month, event, 1)
		
		cpages = soup.find('div', {'id':'comment-paging'}).find_all('a')
		
		page_num = 1
		for cpage in cpages:
			page_num = page_num + 1
			cpage_url = self.bj_url_prefix + cpage['href']
			self.log.info('')
			self.log.info('< page {0} : {1} >'.format(page_num, cpage_url))
			
			self.driver.get(cpage_url)
			html = self.driver.page_source
			
			self.evt_get_comments_type2(html, db, month, event, page_num)
		
			
			
	# 서울 오피 플랜맨 이벤트에 코멘트로 신청한 정보 수집
	def evt_get_comments_type2(self, html, db, month, event, page):
	
		'''

<< 8월 우리동네 안마왕 part1 신청 양식 >>

신청 양식
아이디 : jangddong  닉네임 : 그녀와의추억
1. 강남1구역  2. 서울권1구역
후기링크 : 6~7월 본인이 잘썼다고 생각하는 후기링크~

		'''
	
		soup = BeautifulSoup(html, 'html.parser')
		comments = soup.find_all('li', {'class':'comment_row depth0'})
		
		error_count = 0
		index = 0
		for comment in comments:
			index = index + 1
			if (page == 1 and index == 1): continue
			
			self.log.info('')
			self.log.info('< {0} >'.format(index))
			
			contents = comment.find('textarea').get_text()
			#self.log.info(contents)
			#self.log.info(' ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----')
			
			contents = contents.replace('&nbsp;',' ').replace('[',' [').replace('.','. ').replace(' (','(').replace(':',': ').replace(']','] ').replace('닉네임', ' 닉네임')
			p = re.compile('<p.*?>')
			contents = p.sub('\n', contents)
			p = re.compile('<span.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<div.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<strong.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<font.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<br.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<b.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<a.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('<!.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('</.*?>')
			contents = p.sub(' ', contents)
			p = re.compile('^ *')
			contents = p.sub(' ', contents)
			p = re.compile('^\n')
			contents = p.sub(' ', contents)
			contents = contents.replace('강남','강남 ').replace('역삼 ','역삼 ').replace('선릉 ','선릉 ').replace('상봉','상봉 ').replace('-',' - ')
			contents = contents.strip()
			
			contents = contents.split()
			self.log.info(contents)
			
			id = self.regevt_get_comment_item(contents, '아이디', ':')
			if (id == None): 
				error_count = error_count + 1
				continue
			
			nickname = self.regevt_get_comment_item(contents, '닉네임', ':')
			if (nickname == None): 
				error_count = error_count + 1
				continue
			
			choice = []
			for idx in range(10):
				item_name = u'{0}지망'.format(idx+1)
				temp = self.regevt_get_comment_item2(contents, item_name, '-')
				if (temp == None): break
				choice.append(temp)
				
			#choice1 = choice1.replace('1', ' 1').replace('2', ' 2').replace('3', ' 3')
			
			#choice2 = self.regevt_get_comment_item(contents, '2', '.')
			'''
			if (choice2 == None): 
				error_count = error_count + 1
				continue
			'''
			'''
			choice3 = self.regevt_get_comment_item2(contents, '3', '.')
			if (choice3 == None): 
				error_count = error_count + 1
				continue
			'''
			rank_img = comment.find('div', {'class':'writer'}).find_all('img')
			rank_img = rank_img[len(rank_img)-1]['src']
			rank = self.get_rank_for_image(rank_img)
						
			self.log.info(' - ID: {0}'.format(id))
			self.log.info(' - Nickname: {0}'.format(nickname))
			self.log.info(' - Rank    : {0}'.format(rank))
			
			index = 0
			for ch in choice:
				index = index + 1
				self.log.info(' - Choice {0}: {1}'.format(index, ch[0]))
				db.insert_applications(id, month, event, ch[0], index)
			#	def insert_applications(self, user_id, month, event, shop, ordering):

			#db.insert_applications(id, month, event, choice1, 1)
			'''
			if(choice2 != None): 
				#choice2 = choice2.replace('1', ' 1').replace('2', ' 2').replace('3', ' 3')
				self.log.info(' - Choice 2: {0}'.format(choice2))
				#db.insert_applications(id, month, event, choice2, 2)
			'''
			
			# Insert applicant's information
			#db.add_regular_event_applicant(id, nickname, rank, choice1[0], choice2[0], choice3[0])
			
			#self.get_member_statistics(id, self.check_month)
		
		return index, error_count
		
		
	# bj맛 포인트 순위별로 예상 당첨 업소 출력
	def evt_winning_prediction(self):
		db = bamdb.BamDB()
		ui_list = [list(i) for i in db.get_re_applicant_list()]
		si_list = [list(i) for i in db.get_re_shop_list()]
		
		# 무료권 분배
		for ui in ui_list:
			#print(ui)
			win = False
			for i in range(2,5):
				jimang = ui[i]
				#self.log.info('F:{0}:{1}'.format(ui[0], jimang))
				for si in si_list:
					if (jimang == si[0]):
						#self.log.info(' + {0}'.format(si[1]))
						if (si[1] > 0):
							si[1] = si[1] - 1
							ui.append('{0}/무료권'.format(si[0]))
							win = True
						break
				if (win == True):
					break
	
		# 원가권 분배
		for ui in ui_list:
			if(len(ui) > 6): continue
			win = False
			for i in range(2,5):
				jimang = ui[i]
				#print('C:{0}:{1}'.format(ui[0], jimang))
				for si in si_list:
					if (jimang == si[0]):
						#print(' + {0}'.format(si[2]))
						if (si[2] > 0):
							si[2] = si[2] - 1
							ui.append('{0}/원가권'.format(si[0]))
							win = True
						break
				if (win == True):
					break
			if (win == False):
				ui.append('----------')
					
	
		index = 0
		for ui in ui_list:
			index = index + 1
			#self.log.info('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}'.format(index, ui[0], ui[1], ui[2], ui[3], ui[4], ui[5], ui[6]))
			ui.append( db.get_re_coupon_winning(ui[0], 1 if self.check_month==12 else self.check_month+1) )
			#self.log.info('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}'.format(index, ui[0], ui[1], ui[2], ui[3], ui[4], ui[5], ui[6], db.get_re_coupon_winning(ui[0], 1 if self.check_month==12 else self.check_month+1)))
			ui.append( "OK" if ui[6] == ui[7] else "NOK" )
			
			''' HTML 
			self.log.info('<tr>')
			self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[1]+'</td>')
			#self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+str(ui[4])+'</td>')
			#self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[1]+'</td>')
			#self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[2]+'</td>')
			#self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[3]+'</td>')
			self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[6]+'</td>')
			self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[7]+'</td>')
			self.log.info('<td style="border-style: solid; border-width: 1px; border-color: #000000; color: black; line-height: 2;">'+ui[8]+'</td>')
			self.log.info('</tr>')			
			'''
			self.log.info(ui[1] +' | '+ str(ui[5]) +' | '+ ui[6]  +' | '+ ui[7] +' | '+ ui[8]  )
			
			if (index == 100): break
			
