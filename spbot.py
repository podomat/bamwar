import bjbot


class spbot(bjbot.bjbot):
	def __init__(self, command):
		super().__init__(command)
		
	
	def run(self, board, scan, start):
		page = 0
		completed = False
		started = True
		
		self.close_log()
		self.init_log(board)
		
		if(start != None): started = False
		
		while completed == False:
			page = page + 1
			bo_table = bjbot.shop_bo_table_map[board]
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
				title = ' '.join(x for x in review.find('a', {'class':'link_subject'}).get_text().strip().split('\xa0'))
				
				self.log.info('')
				self.log.info('')
				self.log.info(u'[TITLE]: {0}'.format(title))
				self.log.info(u'[{0}-{1}-{2},{3}] {4}'.format(board, page, index, wr_id, link))
				
				# 베스트글 skip
				if(self.get_post_num(review) == None):
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
				regidate = self.get_regidate(review)
				if(self.is_too_old_review(regidate, 'forComment') == True):
					self.log.info('   >> Skip this post, reason= "Too old article, regidate={0}"'.format(regidate))
					completed = True
					break
				
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
					self.log.info('   >> Skip this post, reason= "There is already my comment."')
					if (scan == True):
						continue
					else: 
						self.log.info('   >> Job complete (simple)')
						completed = True
						break
						
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
