SET @shop = '강남 lock';

SELECT
	user_id as 아이디, 
	nickname as 닉네임, 
	rank as 계급,
	month as 월, 
 	total_post_num as '전체 원글수', 
 	fb_post_num as '자게 원글수', 
 	rb_post_num as '후기수', 
 	eb_post_num as '기타 원글수',
	total_comment_num as '전체 댓글수',
	fb_comt_num as '자게 댓글수',
	rb_comt_num as '후기 댓글수',
	eb_comt_num as '기타 댓글수'
FROM user_info 
WHERE choice1_name = @shop 
OR choice2_name = @shop 
OR choice3_name = @shop
ORDER BY (total_post_num+total_comment_num) DESC