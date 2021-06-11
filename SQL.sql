
# Query 1

select distinct date , sum(prod_price * prod_qty) as ventes 
from transaction
where date > = '01/01/2019'  and date <= '31/12/2019' 
group by date 
order by date
;


# Query 2

select t.client_id ,
(select t.prod_price * t.prod_qty where t.prop_id = tm.product_id) as DECO,
(select t.prod_price * t.prod_qty where t.prop_id = tp.product_id ) as MEUBLE
from transaction t
join product_nomenclature tm on t.prop_id = tm.product_id
join product_nomenclature tp on t.prop_id = tp.product_id 
where  tm.product_type ='DECO' or  tp.product_type ='MEUBLE'
group by t.client_id 
;
