SELECT name,CONCAT('http://localhost:8080/recipe/detail/' ,id) AS URL
FROM recipe
WHERE breakfast_flg = 1
ORDER BY RANDOM()
LIMIT 7;