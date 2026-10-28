# coldchain-pipeline

Cold-chain monitoring for our pharma distribution warehouses. Every night it pulls
temperature readings from two sensor vendors for 3 warehouses, reads door-open
events (a CSV our facility team emails every morning, saved into `inbox/` by an
Outlook rule), and builds the daily compliance report for QA. Every Monday the
ops team gets a KPI spreadsheet.

I built this alone over the last year. Two more warehouses go live in spring and
a customer portal wants the readings through an API. Every change breaks
something: last month QA signed off a day that actually had a 3-hour gap.

Cron: see `crontab.txt`. Database: `data/coldchain.db` (SQLite).
