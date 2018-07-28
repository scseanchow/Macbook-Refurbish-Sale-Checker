import bs4 as bs
import urllib.request
import smtplib
import re

# SIMPLE SCRIPT TO RUN A WEB SCRAPER TASK TO CHECK IF YOUR DESIRED MACBOOK PRO IS ON REFURB AND NOTIFY VIA EMAIL

# example 13 inch
PRODUCT_PAGE = 'https://www.apple.com/ca/shop/browse/home/specialdeals/mac/macbook_pro/13'

# put in your specifications here ie:
# 'CPU': 'quad-core',
# 'RAM': '16GB',
# 'GPU': 'Intel Iris Plus Graphics 655',
# 'RELEASE_DATE': '2017',
MACBOOK_PRO = {
    'CPU': '',
    'RAM': '',
    'GPU': '',
    'RELEASE_DATE': '',
}

# Email / Password
EMAIL_LOGIN = {
    'USERNAME': '',
    'PASSWORD': '',
}

def send_email(product_info):  
    server = smtplib.SMTP('smtp.gmail.com', 587) # gmail address
    server.starttls()
    server.login(EMAIL_LOGIN['USERNAME'], EMAIL_LOGIN['PASSWORD'])
    
    msg = 'Macbook Pro Refurbished Found\n' + product_info
    server.sendmail(EMAIL_LOGIN['USERNAME'], EMAIL_LOGIN['USERNAME'], msg)
    server.quit()


source = urllib.request.urlopen(PRODUCT_PAGE).read()
soup = bs.BeautifulSoup(source,'html.parser')

rows = soup.find_all('tr', {'class': 'product'})
for row in rows:
    cells = row.find_all("td", {'class': 'specs'})
    product_info = str(cells)
    is_found = True
    for key, value in MACBOOK_PRO.items():
        if value.lower() not in product_info.lower():
            is_found = False
            continue
    if is_found:
        product_info = re.sub('<[^<]+?>', '', product_info)
        send_email(product_info)