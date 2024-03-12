from selenium import webdriver
import threading
def cay():
    a = webdriver.Chrome()
    a.get("https://www.youtube.com/watch?v=hud9nXMg52I")
    while True:
        continue
for i in range(10):
    threading.Thread(target=cay).start()
