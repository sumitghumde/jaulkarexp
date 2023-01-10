# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver=webdriver.Chrome(executable_path = "C:\\MIT Data\\chromedriver\\chromedriver.exe")
# driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
# # elements = driver.find_element(By.CLASS_NAME,'resp-tabs-container')
# elements = driver.find_element(By.ID,'gallery')
# # print(elements.get_attribute("class"))
# chld =elements.find_elements(By.TAG_NAME,'div')
# # chld = elements.fi
# for i in chld:
#     # print(i.get_attribute("class"))
#     if str(i.get_attribute("class")=="single_tab_div resp-tab-content resp-tab-content-active"):
#         x=i.find_elements(By.TAG_NAME,'iframe')
#         print(len(x))



#
# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
#
# driver=webdriver.Chrome(executable_path = "C:\\MIT Data\\chromedriver\\chromedriver.exe")
# # to maximize the browser window
# driver.maximize_window()
# #get method to launch the URL
# driver.get("https://www.globalsqa.com/demo-site/draggableboxes/")
# driver.switch_to.frame(driver.find_element(By.XPATH,'//div[@class="single_tab_div resp-tab-content resp-tab-content-active"]//iframe'))
# xsource = driver.find_element(By.ID,"draggable")
# action = ActionChains(driver)
# action.drag_and_drop_by_offset(xsource, 100, 0)

# perform the operation
# from selenium.webdriver.common.by import By
#
# action.perform()
#to refresh the browser
# driver.refresh()
# driver.find_element_by_link_text("Frames").click()
# driver.find_element_by_link_text("Nested Frames").click()
# # to switch to frame with frame name
# driver.switch_to.frame("frame-bottom")
# # to get the text inside the frame and print on console
# print(driver.find_element_by_xpath ("//*[text()='BOTTOM']").text)
# # to move out the current frame to the page level
# driver.switch_to.default_content()
# #to close the browser
# driver.quit()
#
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# import time
# driver=webdriver.Chrome(executable_path = "C:\\MIT Data\\chromedriver\\chromedriver.exe")
# # to maximize the browser window
# driver.maximize_window()
# #get method to launch the URL
# driver.get("https://demo.automationtesting.in/Register.html")
#
# selectskills = Select(driver.find_element(By.XPATH,'//select[@id="Skills"]'))
#
# # selectskills.select_by_value("AutoCAD")
# selectskills.select_by_index(6)
# selectskills.select_by_visible_text("C")
# time.sleep(15)
#
#
# selectcountry = Select(driver.find_element(By.ID,"country"))
# driver.find_element(By.XPATH,'//*[@id="basicBootstrapForm"]/div[10]/div/span').click()
# driver.find_element(By.XPATH,"/html/body/span/span/span[1]/input").send_keys("a")
# driver.find_element(By.XPATH,'//*[@id="select2-country-results"]/li[4]').click()
#

# # selectskills.select_by_visible_text("C")
# time.sleep(15)
# select = Select(driver.find_element_by_id('fruits01'))
#
# # select by visible text
# select.select_by_visible_text('Banana')
#
# # select by value
# select.select_by_value('1')
#
x=50
y=20
m= "yes" if x > y else "no"
print(m)