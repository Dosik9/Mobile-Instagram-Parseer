import csv
from appium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys
import pyperclip as pc
import pandas as pd
import os
import requests

capabilities = {
    "platformName": "Android",
    "platformVersion": "13",
    "appium:deviceName": "emulator-5554",
    # "appium:app": "C:\\Users\\Dosbol\\PycharmProjects\\MobInstaParser\\apps\\instagram-260-0-0-23-115.apk"
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=capabilities)

# Swipe up: for each device, the necessary dimensions for the shape are taken. timeduration - swipe speed
def swipe_up(timeduration:int = 600):
    size = driver.get_window_size()
    starty = int(size['height'] * 0.80)
    endy = int(size['height'] * 0.20)
    startx = int(size['width'] * 0.6)
    endx = startx + 5
    driver.swipe(start_x=startx, start_y=starty, end_x=endx, end_y=endy, duration=timeduration)
    print('swiped up')

# Swipe up: for each device, the necessary dimensions for the shape are taken. timeduration - swipe speed
def swipe_down(timeduration:int = 800):
    size = driver.get_window_size()
    starty = (int)(size['height'] * 0.20)
    endy = (int)(size['height'] * 0.85)
    startx = size['width'] / 2
    endx = startx
    # print(f'startx: {startx} \tstarty: {starty} \nendx: {endx} \tendy: {endy}')
    driver.swipe(startx, starty, endx, endy, timeduration)
    print('swiped down')

# Swipe up: for each device, the necessary dimensions for the shape are taken. timeduration - swipe speed
def swipe_right(timeduration:int = 0):
    size = driver.get_window_size()
    # print(f'screen size: {size}')
    starty = int(size['height'] / 2)
    endy = starty
    startx = int(size['width'] * 0.1)
    endx = int(size['width'] * 0.9)
    # print(f'startx: {startx} \tstarty: {starty} \nendx: {endx} \tendy: {endy}')
    driver.swipe(startx, starty, endx, endy, timeduration)
    print('swiped right')

# Swipe up: for each device, the necessary dimensions for the shape are taken. timeduration - swipe speed
def swipe_left(timeduration:int = 0):
    size = driver.get_window_size()
    # print(f'screen size: {size}')
    starty = int(size['height'] / 2)
    endy = starty
    startx = int(size['width'] * 0.9)
    endx = int(size['width'] * 0.1)
    # print(f'startx: {startx} \tstarty: {starty} \nendx: {endx} \tendy: {endy}')
    # print("Start swipe operation")
    driver.swipe(startx, starty, endx, endy, timeduration)
    print('swiped left')

#Open the instagram: this function searches instagram on the home page and on the first work page
def open_insta():
    if (len(driver.find_elements(By.XPATH, '//android.widget.TextView[@content-desc="Instagram"]')) >0):
        print("FOUND")
        driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Instagram"]').click()
    else:
        print("NOT FOUND!")
        driver.press_keycode(3)
        time.sleep(2)
        swipe_up()
        open_insta()

# Find account: for this function will be work, the Instagram must be opened and the search button (magnifying glass icon) must be visible
def find_acc():
    driver.find_element(By.ID, 'com.instagram.android:id/search_tab').click()
    driver.find_element(By.ID, 'com.instagram.android:id/action_bar_search_edit_text').click()
    time.sleep(2)
    username = input('Who do you want to find? ')
    search_acc = driver.find_element(By.ID, 'com.instagram.android:id/action_bar_search_edit_text')
    search_acc.clear()
    search_acc.send_keys(username)
    search_acc.send_keys(Keys.ENTER)
    time.sleep(2)
    accs = driver.find_elements(By.ID, 'com.instagram.android:id/row_search_user_username')
    for acc in accs:
        if acc.text == username:
            acc.click()
            break

#Open the first post: must be opened profile of user with post
def open_thefirst_post():
    first_row = driver.find_element(By.ID, 'com.instagram.android:id/media_set_row_content_identifier')
    first_column = first_row.find_element(By.CLASS_NAME, 'android.widget.Button')
    first_column.click()

#Like the post: like button (heart icon) must be visible
def like_it():
    driver.find_element(By.ID, 'com.instagram.android:id/row_feed_button_like').click()

#Get URL of post: Get URL of post which have 3 points
def url_of_post():
    username = driver.find_element(By.ID, 'com.instagram.android:id/row_feed_photo_profile_name').text
    username = username.strip()
    driver.find_element(By.ID, 'com.instagram.android:id/feed_more_button_stub').click()
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ImageView').click()
    time.sleep(2)
    post_url = pc.paste()
    print(post_url)
    r = requests.get(post_url)
    if not os.path.exists(username):
        os.makedirs(username)
        print('U vas okazyvaetsa net neobhodimoi papki. \nDavaite sperva sozdadim')

    with open(f'{username}/links of posts.txt', 'a') as f:
        f.write(r.content)

#Parse follows: This function can parse followers and followings, and parse in deep
def parse_follows(choice, step: int = 0, follows: dict = {}, deep: int = 1, file_name: str = ''):
    adams = []
    if len(follows) == 0:
        follows = {'Adamdar': [], 'Step': []}

    start_time = time.time()
    username = driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text

    if not os.path.exists(f'{choice}'):
        os.makedirs(f'{choice}')
        print('U vas okazyvaetsa net neobhodimoi papki. \nDavaite sperva sozdadim ee')
        loading = ''
        for i in 'Loading...':
            time.sleep(3)
            loading += i
            print(loading)

    file_name = file_name

    if step == 0:
        follows['Adamdar'].append(username)
        follows['Step'].append(step)
        follows_csv = pd.DataFrame(follows)
        file_name = f'{choice}/{username}_#deep-{deep}.csv'
        follows_csv.to_csv(f'{file_name}', index=False)

    if len(driver.find_elements(By.ID, 'com.instagram.android:id/row_profile_header_empty_profile_notice_container')) < 1:
        driver.find_element(By.ID, f'com.instagram.android:id/row_profile_header_{choice}_container').click()
        time.sleep(0.75)
        print('Clicked')
        step += 1

        while True:
            i = 0
            while True:
                if (len(driver.find_elements(By.ID, 'com.instagram.android:id/follow_list_username')) > 0) & (len(driver.find_elements(By.ID, 'com.instagram.android:id/follow_list_username')) != i):
                    users = driver.find_elements(By.ID, 'com.instagram.android:id/follow_list_username')
                    adam = users[i].text.strip()
                    adams.append(adam)
                    follows['Adamdar'].append(adam)
                    follows['Step'].append(step)
                    if deep == step:
                        print('zdes`')
                        new_row = pd.DataFrame({'Adamdar': adam, 'Step': step}, index=[0])
                        new_row.to_csv(file_name, header=None, mode='a', index=False)
                    elif step < deep:
                        users[i].click()
                        time.sleep(0.75)
                        if len(driver.find_elements(By.ID,'com.instagram.android:id/row_profile_header_empty_profile_notice_container')) < 1:
                            df = pd.read_csv(file_name)
                            df = df.drop_duplicates(subset='Adamdar')
                            name = driver.find_element(By.ID, 'com.instagram.android:id/action_bar_title').text.strip()
                            if name in df.values:
                                print(df.loc[df['Adamdar'] == name]['Step'])
                                if df.loc[df['Adamdar'] == name]['Step'].values[0] >= step:
                                    continue
                            new_row = pd.DataFrame({'Adamdar': adam, 'Step': step}, index=[0])
                            new_row.to_csv(file_name, header=None, mode='a', index=False)
                            parse_follows(choice, step, follows, deep, file_name)
                            driver.back()
                            time.sleep(0.75)

                        else:
                            new_row = pd.DataFrame({'Adamdar': adam, 'Step': step}, index=[0])
                            new_row.to_csv(file_name, header=None, mode='a', index=False)
                            print('osynda')
                            continue
                    else:
                        print('Ya tut!')

                    print('ne bolyp jatyr')
                elif len(driver.find_elements(By.ID, 'com.instagram.android:id/follow_list_username')) == i:
                    if len(driver.find_elements(By.ID, 'com.instagram.android:id/row_load_more_button')) > 0:
                        driver.find_element(By.ID, 'com.instagram.android:id/row_load_more_button').click()
                        time.sleep(0.75)
                    swipe_up()
                    i = 0
                else:
                    print('break')
                    break
                i += 1
                adams = list(set(adams))
                print(len(list(set(adams))))
                print('tut')
                # driver.back()
            break
        driver.back()
        time.sleep(0.75)
        print(follows)
        print(step)
        step -= 1
    else:
        follows['Adamdar'].append(username)
        follows['Step'].append(step)
        new_row = pd.DataFrame({'Adamdar': username, 'Step': step}, index=[0])
        new_row.to_csv(file_name, header=None, mode='a', index=False)
        # follows['account_type'].append('private')

    if step == 0:
        follows = pd.DataFrame(follows)
        follows = follows.drop_duplicates(subset=['Adamdar'])
        # follows.to_csv(f'{choice}/{username}_#deep-{deep}.csv', index=False)
        fs_count = len(follows)
        end_time = time.time()
        print(f'Start time: {start_time} \nEnd_time: {end_time} \nProcess time: {round((end_time-start_time),2)} \nSpend for each account: {round(((end_time-start_time)/int(fs_count)),2)} seconds')

    return follows

def menu():
    print('\t*****MENU*****\n')
    print('[1].BACK')
    print('[2].SWIPE DOWN')
    print('[3].LIKE THE POST')
    print('[4].SWIP LEFT')
    print('[5].GET THE URL OF THE POST')
    print('[6].SWIPE RIGHT')
    print('[7].FIND ACCOUNT')
    print('[8].SWIPE UP')
    print('[9].OPEN THE FIRST POST')
    print('[0].OPEN THE INSTAGRAM')
    print('[followers].To get followers from this account')
    print('[following].To get followings from this account\n')

while True:
    menu()
    button = input('Input command for action: ').lower()
    if button == "8":
        swipe_up()
    elif button == '2':
        swipe_down()
    elif button == '6':
        swipe_right()
    elif button == '4':
        swipe_left()
    elif button == '5':
        url_of_post()
    elif button == '0':
        open_insta()
    elif button == '1':
        driver.back()
    elif button == '7':
        find_acc()
    elif button == '9':
        open_thefirst_post()
    elif button == '3':
        like_it()
    elif button == 'followers':
        deep = int(input('Enter count of deep: '))
        parse_follows(button, deep=deep)
        break
    elif button == 'following':
        deep = int(input('Enter count of deep: '))
        parse_follows(button, deep=deep)
        break
    else:
        break
