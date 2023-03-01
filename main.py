from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import os

# 你的資訊
url = "https://www.facebook.com/"
email = ""
password = ""

# 設置Chrome的啟動選項
chrome_options = Options()
chrome_options.add_argument("--incognito")

# 使用ChromeDriverManager自動下載chromedriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# 最大化視窗
driver.maximize_window()
# 進入Facebook登入畫面
driver.get(url)

# 填入帳號密碼，並送出
driver.find_element(By.ID, "email").send_keys(email)
driver.find_element(By.ID, "pass").send_keys(password)
driver.find_element(By.NAME, "login").click()

time.sleep(5)



url = f"https://www.facebook.com/FEBigCity"
response = requests.get(url)
html = response.text

# 進入木棉花專頁
driver.get("https://www.facebook.com/emuse.com.tw")

time.sleep(5)

# 往下滑3次，讓Facebook載入文章內容
for x in range(1):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    print("scroll")
    time.sleep(5)

root = BeautifulSoup(driver.page_source, "html.parser")

# 定位文章標題
titles = root.find_all(
    "div", class_="x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld")
for title in titles:
    # 定位每一行標題
    posts = title.find_all("div", dir="auto")
    # 如果有文章標題才印出
    if len(posts) != 0:
        for post in posts:
            print(post.text)

    likes = title.find_all("span", class_="xt0b8zv x1jx94hy xrbpyxo xl423tq")
    # 獲取第一個元素的文本
    if len(likes) != 0:
        for like in likes:
            print(like.text)

    print("-" * 30)
    
# 建立資料夾
if not os.path.exists("images"):
    os.mkdir("images")

# 下載圖片
images = root.find_all(
    "img", class_=["x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"])
if len(images) != 0:
    for index, image in enumerate(images):
        img = requests.get(image["src"])
        with open(f"images/img{index+1}.jpg", "wb") as file:
            file.write(img.content)
        print(f"第 {index+1} 張圖片下載完成!")

tool_bar_element = driver.find_element(By.XPATH,'//div[@role="button"]')
tool_bar_element.click()

# 等待5秒
time.sleep(5)
# 關閉瀏覽器
driver.quit()