from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import xlsxwriter as xl

### User Input ###
email = 'walker3791@gmail.com'
password = 'Starfishes7'
base_num = '31955'

##### Structures ID's #####
mr = 'item_metal-refineries'
mr_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Metal Refineries']"
sol = 'item_solar-plants'
sol_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Solar Plants']"
urb = 'item_urban-structures'
urb_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Urban Structures']"
rf = 'item_robotic-factories'
rf_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Robotic Factories']"
sp = 'item_spaceports'
sp_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Spaceports']"
sy = 'item_shipyards'
sy_action = "//form[@action='base.aspx?base=" + base_num + "&view=structures&action=upgrade&item=Shipyards']"

### DEFINITIONS ###
# Build structure
def build(soup, build_order, build_action):
	# Find time to build
	div = soup.find(id=build_order)
	print('build_order: ' + build_order)
	time_wait = div.find(class_='time').get_text()
	sec_wait = int(time_wait[:-5]) * 60 + int(time_wait[-3:-1])
	print(time_wait)
	print(sec_wait)

	# Build structure and wait
	print('Building address: ' + build_action)
	elem = driver.find_element_by_xpath(build_action)
	elem.click()
	time.sleep(sec_wait+5)
	driver.refresh()
	print(build_order + 'built.')

def build_resource(soup, build_order, build_action):
	# Go to Support tab
	elem = driver.find_elements_by_link_text('Support')[1]
	elem.click()

	# Find time to build
	div = soup.find(id=build_order)
	print('build_order: ' + build_order)
	time_wait = div.find(class_='time').get_text()
	sec_wait = int(time_wait[:-5]) * 60 + int(time_wait[-3:-1])
	print(time_wait)
	print(sec_wait)

	# Build structure and wait
	print('Building address: ' + build_action)
	elem = driver.find_element_by_xpath(build_action)
	elem.click()
	time.sleep(sec_wait+5)
	driver.refresh()
	print(build_order + 'built.')

	# Go to Facilites tab
	elem = driver.find_element_by_link_text('Facilities')
	elem.click()

# Check Resources
def resource_check(soup):
	# Check population
	pop_fraction = soup.find(title='Population').get_text()
	print(pop_fraction)
	if len(pop_fraction) <= 5:
		pop = pop_fraction[:-3]
		pop_limit = pop_fraction[-2::]
	else:
		pop = pop_fraction[:-4]
		pop_limit = pop_fraction[-3::]

	# Check energy
	energy_fraction = soup.find(title='Energy').get_text()
	print(energy_fraction)
	if len(energy_fraction) <= 5:
		energy = energy_fraction[:-3]
		energy_limit = energy_fraction[-2::]
	else:
		energy = energy_fraction[:-4]
		energy_limit = energy_fraction[-3::]

	# Check area
	#area_fraction = soup.find(title='Area').get_text()
	#print(area_fraction)
	#if len(area_fraction) <= 5:
		#area = area_fraction[:-3]
		#area_limit = area_fraction[-2::]
	#else:
		#area = area_fraction[:-4]
		#area_limit = area_fraction[-3::]

	# Build support structures if necessary
	if pop == pop_limit:
		build_resource(soup, urb, urb_action)
	elif energy == energy_limit:
		build_resource(soup, sol, sol_action)
	#if area == area_limit:
		#build(soup, ter, ter_action)
	######

### SETTING UP SELENIUM DRIVER ###
driver = webdriver.Chrome(executable_path=r"C:\Users\wneal\Documents\Stuff\Python\chromedriver_win32\chromedriver.exe")

# Getting initial page
driver.get('https://mystic.astroempires.com/base.aspx?base=' + base_num + '&view=structures')

# Logging in
elem = driver.find_element_by_name('email')
elem.send_keys(email)
elem = driver.find_element_by_name('pass')
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

# Transferring html to BS
soup = BeautifulSoup(driver.page_source, 'lxml')

# Building order
build_order = [mr, mr, mr, mr, mr, mr, rf, sp, sy, mr, rf, sp, sy, mr, rf, sp, sy, mr, rf, sp, sy, mr, rf, sp, sy]
build_action = [mr_action, mr_action, mr_action, mr_action, mr_action, mr_action, rf_action, sp_action, sy_action, mr_action, rf_action, sp_action, sy_action, mr_action, rf_action, sp_action, sy_action, mr_action, rf_action, sp_action, sy_action, mr_action, rf_action, sp_action, sy_action]

# Building Loop
for x in range(0,26):

	driver.get('https://mystic.astroempires.com/base.aspx?base=' + base_num + '&view=structures')
	soup = BeautifulSoup(driver.page_source, 'lxml')



	#if build_order[x] == sol:
	#	elem = driver.find_elements_by_link_text('Support')[1]
	#	elem.click()
	#elif build_order[x] == urb:
	#	elem = driver.find_elements_by_link_text('Support')[1]
	#	elem.click()
	#else:
	#	elem = driver.find_element_by_link_text('Facilities')
	#	elem.click()

	# Check resources
	resource_check(soup)

	# Build structure and wait
	build(soup, build_order[x], build_action[x])
	



