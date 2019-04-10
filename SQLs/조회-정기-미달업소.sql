-- 무료권 미달 업장 --
select name as 이름, category as 업종, cost_coupon as 원가권, free_coupon as 무료권, choice1 as '1지망', choice2 as '2지망', choice3 as '3지망'
from re_shops 
where (@a := (choice1+choice2+choice3)) < free_coupon
order by category asc
