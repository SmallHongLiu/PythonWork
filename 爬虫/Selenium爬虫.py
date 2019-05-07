from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytesseract

'''这里填刚刚下载的驱动的路径f'''
chrome_driver = "/Applications/Google Chrome.app/Contents/MacOS/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver)

url = 'http://hotel.qunar.com/city/beijing_city/'
driver.get(url)

time.sleep(6)  # 等待页面加载完再进行后续操作

'''在页面顶部，底部各找一个元素，并模拟鼠标从顶到底的滑动'''
start = driver.find_element_by_class_name('e_above_header')
target = driver.find_element_by_class_name('qn_footer')
ActionChains(driver).drag_and_drop(start, target).perform()

time.sleep(5)  # 等待页面加载完再进行后续操作

hotel_link_list = driver.find_elements_by_css_selector("[class='item_price js_hasprice']")
print('在此页面共有酒店: ', len(hotel_link_list), '家')
windows = driver.window_handles

# 此处可以爬取整个页面任何想要的元素
list_hotel_info = []

def hotel_info_clawer():
    list_hotel_info.append([driver.find_element_by_class_name('info').text,
                            driver.find_element_by_class_name('js-room-table').text,
                            driver.find_element_by_class_name('dt-module').text])

for i in range(len(hotel_link_list)):
    hotel_link_list[i].click()
    driver.switch_to.window(windows[-1])  # 切换都刚打开的酒店详情页
    hotel_info_clawer()
    driver.close()  # 关闭已经爬完的酒店详情页
    print('已经爬取酒店: ', i , '家')



