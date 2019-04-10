select w.user_id, u.nickname, concat(w.shop, '/', w.`type`) as shop, u.point from coupon_winning w, user_info u 
where w.event = '정기' 
and w.month = 10 
and w.user_id = u.user_id
order by u.point desc 
limit 100