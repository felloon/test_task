# Test task.

Test task for a job vacancy. This application simulates the operation of a platform designed for customer support
representatives who handle user requests.

## Features.

1. Users:
    * Create chats;
    * Send message in active chat;
    * Set CSAT to closed chat.
2. Operators:
    * Can reply to message by user;
    * Closing chat.

## Requirements.

* Python 3.13.5 or higher.

## Install guide.

1. Pull the repo.

```bash
git clone https://github.com/felloon/test_task.git
cd test_task
```

2. Run project.

```bash
py -m main
```

## SQL tasks.

Task а:

```
SELECT ticket_client FROM tickets
WHERE csat < 3
```

Task б:

```
SELECT ticket_id FROM tickets
WHERE text LIKE '%отлично%'
ORDER BY csat DESC
```

Task в:

```
SELECT COUNT(place), MAX(price) as max_sum, order_client_id as frequent_customer
FROM orders
WHERE (place = 'Теремок' and price >= 2000 and price <= 10000) or (place = 'Вкусно и точка' and price >= 2000 and price <= 10000)
GROUP BY order_client_id
HAVING COUNT(place) > 5
```

Task г:

```
SELECT * FROM orders as o
JOIN clients as c ON o.order_client_id = c.client_id
JOIN tickets as t ON o.order_id = t.ticket_order_id
LIMIT 1000
```