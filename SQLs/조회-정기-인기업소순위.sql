-- 인기 업장 순위 --
select name, category, cost_coupon, free_coupon, choice1, choice2, choice3, (cost_coupon+free_coupon) as sum_coupon, (choice1+choice2+choice3) as sum_choice,
(choice1+choice2+choice3)/(cost_coupon+free_coupon) as coupon_rate,
(choice1+choice2+choice3)/(free_coupon) as free_rate 
from re_shops 
order by (choice1+choice2+choice3) desc limit 20