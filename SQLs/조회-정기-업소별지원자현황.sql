set @shop_name='강남 시티';
set @month=3;

select user_id, nickname, rank, choice1_name, choice2_name, choice3_name, point, fb_post_num, fb_comt_num from user_info where month = @month and user_id in 
(select user_id from re_applicants where choice1_name = @shop_name or choice2_name = @shop_name or choice3_name = @shop_name)
order by point desc, fb_post_num desc, fb_comt_num desc