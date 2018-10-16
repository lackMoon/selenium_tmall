from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from multiprocessing import Process,Queue
import time
import pymysql
def parse_page(products):
	browser=webdriver.Firefox()
	wait=WebDriverWait(browser,10)
	totalpage=72
	for page in range(1,totalpage+1):
		time.sleep(1)
		browser.get("https://list.tmall.com/search_product.htm?totalPage=72&user_id=725677994&cat=51454011&jumpto="+str(page))
		product_page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.mainItemsList ul.product-list .product")))
		for product in product_page:
			product_info={}
			title=product.find_element_by_css_selector("div.productInfo h3.product-title >a").text
			sale=product.find_element_by_css_selector("div.productInfo div.item-summary div.item-sum >strong").text
			price=product.find_element_by_css_selector("div.productInfo div.item-summary div.item-price span.ui-price >strong").text
			product_info["title"]=title
			product_info["sale"]=sale
			product_info["price"]=price
			products.put(product_info)
	print("页面爬取完毕")
def savedata(products):
	try:
		connect=pymysql.connect(host="127.0.0.1",user="root",passwd="643120",db="tmall",charset="utf8")
		cur=connect.cursor()
	except Exception as e:
		print(e)
	while True:
		time.sleep(5)
		if not products.empty():
			break
	while not products.empty():
		time.sleep(0.8)
		info=products.get()
		try:
			wood_table="insert into woods(title,sale,price) values('%s','%s','%s');" % (info["title"],info["sale"],info["price"])
			cur.execute(wood_table)
			connect.commit()
		except Exception:
			pass
	cur.close()
	connect.close()
	print("数据导入完毕")
if __name__ == '__main__':
	products=Queue()
	parse=Process(target=parse_page,args=(products,))
	save=Process(target=savedata,args=(products,))
	parse.start()
	save.start()
	parse.join()
	save.join()