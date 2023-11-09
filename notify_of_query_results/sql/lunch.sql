SELECT name,CONCAT('http://localhost:8080/recipe/detail/' ,id) AS URL
FROM recipe
WHERE lunch_flg = 1
ORDER BY RANDOM()
LIMIT 7;