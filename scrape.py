from bs4 import BeautifulSoup
import time
import urllib

def getDomSoup(link):
	return BeautifulSoup(urllib.urlopen(link).read(), 'lxml')

def getProductImage(soup):
	for link in soup.find_all("img"):
		link = link.get('src')
		if link.find('categories') != -1:
			return url + link

def getProductMeta(soup, className, productImageURL):
	for link in soup.find_all('tr', class_ = className):
		#get product name
		productID = link.find(class_ = "productListing-data").string;
		print('productID : ' + productID)
		#get description
		description = link.find(class_ = "listingDescription").string;
		print('Description : ' + description)
		#get description
		name = link.a.string;
		print('name :' + name + '\n')
		#get price
		pricelist = link.find_all("td", {"class": "productListing-data"})
		price = pricelist[3].text
		print('price :' + price)	
     		writeCSV(productID + ',' + name + ',' + description + ',' + productImageURL + ',' + price)

def isProductPage(soup):
	checkValidate_1 = soup.find(class_ = 'productListing-odd')

	if checkValidate_1:
		return True

	checkValidate_2 = soup.find(class_ = 'productListing-odd')

	if checkValidate_1:
		return True

	return False

def getMenuLinks(url):
	global productCount
	soup = BeautifulSoup(urllib.urlopen(url).read(), 'lxml')
	links = []

	for link in soup.find_all(class_ = 'categoryListBoxContents'):

		menu_link = link.a.get('href');

		if menu_link.find('Path=') == -1:
			continue

		print('Processing Link ... : ' + '\n' + menu_link)

		soup = getDomSoup(menu_link)

		#wait until next to avoid blocking
		time.sleep( 2 )

		if isProductPage(soup):
			print('Product page, scrapping data...');
			productImageURL = getProductImage(soup)
			getProductMeta(soup, 'productListing-odd', productImageURL)
			getProductMeta(soup, 'productListing-even', productImageURL)
			productCount += 1
			print('Scrapped Products ')
			print(productCount)

		else :
			print('Not a product page, getting next one...' + '\n');
			getMenuLinks(menu_link)


def writeCSV(productMeta):
	fp.write(productMeta + '\n')

url = 'http://solidspot.com/shop/'

print('Starting script...')

print('Opened new file...')

productCount = 0;

fp = open('solidspot_products.csv','w');

getMenuLinks(url)


print('End scriping...')

fp.close()

print('File closed.')
