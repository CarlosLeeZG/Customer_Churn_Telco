use ai300_capstone;

SELECT * 
	FROM customer c
	LEFT JOIN account a
		USING (customer_id)
	LEFT JOIN account_usage au
		USING(account_id)
	LEFT JOIN city
		USING(zip_code)
	LEFT JOIN churn_status as cs
		USING(customer_id)
	ORDER BY c.customer_id, a.account_id