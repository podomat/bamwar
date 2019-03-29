#-*- coding: utf-8 -*-

import sys
import bjbot
import rebot
import blbot


def show_help():
	print('Usage: {0} <rvt|frac|rvac> [full|simple] [start] [start-page]'.format(sys.argv[0]))
	print('      rvt  : review trawler')
	print('      frac <simple|full> <user_id> [start] [start-page]: freeboard auto-comment')
	print('      rvac : review auto-comment')
	print('      srac : review auto-comment to specific board, ex.) svac ANMA simple 1232345')
	print('      spac : shop profile auto-comment, ex.) spac simple ANMA 1234565')
	print('      reag : regular event information gathering')
	print('      usg <month> <user_id>: user statistics gathering')
	print('      ba <user_id> <link> <comment>: bullet auto-gathering')
	print('      bas <user_id>: bullet auto-gathering shop information')
	print('      bals <user_id> <fname>: bullet auto-gathering for list file')
	

if __name__ == '__main__':
	start = None
	start_page = None

	if ((len(sys.argv) < 2) or (len(sys.argv) > 6)):
		show_help()
		sys.exit(0)
		
	command = sys.argv[1]
	
	if (command == 'reag' or command == 'usg' or command == 'rew' or command == 'wdap1' or command == 'sop' or command == 'pred'):
		bot = rebot.rebot(command, None)
	elif (command == 'frac'):
		bot = bjbot.bjbot(command, sys.argv[3])
	elif (command == 'ba' or command == 'bas' or command == 'bals'):
		bot = blbot.blbot(command, sys.argv[2])
	else:
		bot = bjbot.bjbot(command, None)
	
	if (command != 'pred'):
		bot.init_driver()
		bot.login()
	
	if (command == 'rvt'):
		#bot.run_trawl('HUE_GYONGGI', '수원')
		bot.run_trawl('OP_GYONGGI', '동탄')
		
	elif (command == 'frac'):
		if(len(sys.argv) == 5):
			start = sys.argv[4]
		elif(len(sys.argv) == 6):
			start = sys.argv[4]
			start_page = sys.argv[5]
			
		if (sys.argv[2] == 'full'):
			scan = True
		elif (sys.argv[2] == 'simple'):
			scan = False
		else:
			show_help()
			sys.exit(0)
			
		bot.run_freeboard_auto_comment(scan, start, start_page)
		
	elif (command == 'rvac'):
		if(len(sys.argv) == 4):
			start = sys.argv[3]
			
		if (sys.argv[2] == 'full'):
			scan = True
		elif (sys.argv[2] == 'simple'):
			scan = False
		else:
			show_help()
			sys.exit(0)
		bot.run_all_review_auto_comment(scan, start)
		
	elif (command == 'srac'):
		board = sys.argv[2]
		if(len(sys.argv) == 5):
			start = sys.argv[4]
			
		if (sys.argv[3] == 'full'):
			scan = True
		elif (sys.argv[3] == 'simple'):
			scan = False
		else:
			show_help()
			sys.exit(0)
		bot.run_reviewboard_auto_comment(board, scan, start)
		
		'''
		elif (sys.argv[1] == 'spac'):
			board = sys.argv[2]
			if(len(sys.argv) == 5):
				start = sys.argv[4]
				
			if (sys.argv[3] == 'full'):
				scan = True
			elif (sys.argv[3] == 'simple'):
				scan = False
			else:
				show_help()
				sys.exit(0)
		'''
	
	elif (command == 'spac'):
		bot.add_comment_to_all_shop()
		
	elif (command == 'reag'):
		# bot.regevt_get_shops('http://www.bamwar12.net/bbs/board.php?bo_table=300030&wr_id=11701071&cpage=1#cs') # 18년 8월
		# bot.regevt_get_shops('/bbs/board.php?bo_table=300030&wr_id=12304153&cpage=1#cs') # 18년 9월
		# bot.regevt_get_shops('/bbs/board.php?bo_table=300030&wr_id=12979305&cpage=1#cs') # 18년 10월
		# bot.regevt_get_shops('/bbs/board.php?bo_table=300030&wr_id=13721030&cpage=1#cs') # 18년 11월
		bot.regevt_get_shops('/bbs/board.php?bo_table=300030&wr_id=16755874&cpage=1#cs',
		'https://docs.google.com/spreadsheets/d/e/2PACX-1vQS7FJJ1JNIgXtdTyMf0XCRTjUwDGVdQrYI1z-WIzDh_m1YxEp2xz7Z37okFXEDbQf3seN6upSEQUdH/pubhtml')
		
	elif (command == 'usg'):
		if (len(sys.argv) != 4):
			show_help()
			sys.exit(0)
			
		month = sys.argv[2]
		user_id = sys.argv[3]
		bot.get_member_statistics(user_id, int(month))
		
	elif (command == 'test'):
		#bot.test_get_partner_name('/bbs/board.php?bo_table=300030&wr_id=12526781&sca=후기홍보')
		bot.test()
		
	
	elif (command == 'rew'):
		#bot.gethering_re_winner_info('http://www.bamwar12.net/bbs/board.php?bo_table=000060&wr_id=149018') # 18년 8월
		#bot.gethering_re_winner_info('/bbs/board.php?bo_table=000060&wr_id=155454') # 18년 9월
		bot.gethering_re_winner_info('/bbs/board.php?bo_table=000060&wr_id=161043') # 18년 10월
		
	elif (command == 'wdap1'):
		bot.gethering_uda('http://www.bamwar13.net/bbs/board.php?bo_table=400070&wr_id=959187&cpage=1#cs')	
		
	elif (command == 'sop'):
		bot.gethering_soplan('http://www.bamwar13.net/bbs/board.php?bo_table=400010&wr_id=1037959&cpage=1#cs')
		
	elif (command == 'pred'):
		bot.evt_winning_prediction()
		
	elif (command == 'ba'):
		bot.mine_bullet(sys.argv[3], sys.argv[4], True)
		
	elif (command == 'bas'):
		bot.mine_bullet_shops()
		
	elif (command == 'bals'):
		bot.mine_bullet_list(sys.argv[3])
		
	else:
		show_help()