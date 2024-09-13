from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time


def show_queue(driver):
    e = driver.find_element(By.CSS_SELECTOR,"ytmusic-player-page#player-page")
    if not e.is_displayed():
        print("show_queue")
        driver.find_element(By.TAG_NAME, "body").send_keys("q")

def skip(driver):
    show_queue(driver)
    driver.find_element(By.TAG_NAME, "body").send_keys("j")

def stop(driver):
    show_queue(driver)
    driver.find_element(By.TAG_NAME, "body").send_keys(";")

def queue(driver, query):
    e = driver.find_element(By.CSS_SELECTOR,"input.ytmusic-search-box")
    print(e)
    e.clear()
    e.send_keys(query + "\n")

    try:
        e = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytmusic-search-page .main-action-container ytmusic-menu-renderer button")))
        print("button", e)
        print("button location", e.location)
        print("button is_displayed", e.is_displayed())
        e.click()
    except TimeoutException:
        try:
            e = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytmusic-search-page .main-action-container button")))
            print("menu next button", e)
            e.click()
            e = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#primary ytmusic-menu-renderer button")))
            print("Maybe Album", e)
            e.click()
        except TimeoutException:
            es = driver.find_elements(By.CSS_SELECTOR,"ytmusic-responsive-list-item-renderer")
            for e in es:
                if e.is_displayed():
                    ActionChains(driver).context_click(e).perform()
                    print("select ytmusic-responsive-list-item-renderer")
                    break

    e = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-listbox#items")
    print("popup", e)
    print("popup location", e.location)
    print("popup is_displayed", e.is_displayed())
    qs = e.find_elements(By.TAG_NAME, "yt-formatted-string")
    for e in qs:
        print("queue", e)
        print("queue location", e.location)
        print("queue is_displayed", e.is_displayed())
        print("queue text:", e.text)
        if e.text == "Add to queue" or e.text == "キューに追加":
            e.click()
            break

    time.sleep(1)

    show_queue(driver)

    time.sleep(2)

def openYouTubeMusic():
    options = Options()
    # options.add_argument("--user-data-dir=/home/user/.config/google-chrome")
    # options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    driver.get('https://music.youtube.com/')
    return driver

def closeYouTubeMusic(driver):
    driver.quit()

def main():
    driver = openYouTubeMusic()

    time.sleep(1)

    queue(driver, "斜陽")

    time.sleep(2)

    queue(driver, "デイネイ")

    time.sleep(2)

    queue(driver, "くるり")

    time.sleep(2)

    queue(driver, "NEW ROMANCER 理芽")

    # driver.find_element(By.TAG_NAME, "body").send_keys("?")
    time.sleep(5)
    driver.find_element(By.TAG_NAME, "body").send_keys("j")
    time.sleep(5)
    driver.find_element(By.TAG_NAME, "body").send_keys("k")
    # driver.find_element(By.TAG_NAME, "body").send_keys("q")
    # driver.find_element(By.TAG_NAME, "body").send_keys(";")

    time.sleep(10)

    closeYouTubeMusic(driver)

if __name__ == '__main__':
    main()
