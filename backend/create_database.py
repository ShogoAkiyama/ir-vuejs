import os
import numpy as np
from datetime import datetime as dt
from database import SessionLocal, Company #, Price

company_list = []

with open("./data/company.csv") as f:
    line = f.readline()
    while line:
        company_list.append(line.strip().split(','))
        line = f.readline()

# insert company
db = SessionLocal()
companys = []
for i, comp in enumerate(company_list):
    if i % 100 == 0:
        print(i)
    # insert price
    price_list = []
    with open(os.path.join('./data', 'stock_data', comp[0] + '.T.csv')) as f:
        line = f.readline()
        while line:
            price_list.append(line.strip().split(','))
            line = f.readline()

    # prices = []
    # prev_price = None
    # for price in price_list:
    #     if prev_price is not None:
    #         r = (float(price[1]) - prev_price) / prev_price
    #         prices.append(
    #             {'date': dt.strptime(price[0], '%Y/%m/%d'), 'close': float(price[1]),
    #              'r': r, 'volume': int(float(price[2])), 'company_id': i+1}
    #         )
    #     prev_price = float(price[1])
    # print(prices)

    company = {'code': comp[0], 'name': comp[1], 'industry17': comp[2],
               'industry33': comp[3], 'scale': comp[4]}
    companys.append(company)

db.execute(Company.__table__.insert(), companys)
    # db.execute(Price.__table__.insert(), prices)
db.commit()

db.close()
