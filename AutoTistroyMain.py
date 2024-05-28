import os
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import requests
import urllib
import numpy as np
import cv2  # pip install opencv-python
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random

def txtTopic(folder,txt_file):
    with open(folder+'/'+txt_file, "r", encoding="UTF-8") as f_input:
        topic_list = json.load(f_input)

    try:
        topic = topic_list['topic_list'][0] # 리스트에서 첫 번째 요소 추출
        topic_new_list = {'topic_list': topic_list['topic_list'][1:]} # 나머지 요소를 다시 딕셔너리로 저장
    except:
        print('주제가 없습니다. 생성하고 다시 실행해주세요.')
        time.sleep(5)
        exit()

    with open(folder+'/'+txt_file, "w", encoding="UTF-8") as file:
        json.dump(topic_new_list, file)

    return topic

def txtReading(folder,txt_file):
    set_text = []
    if os.path.exists(folder+'/'+txt_file):
        with open(folder+'/'+txt_file, "r", encoding="UTF-8") as f:
            for line in f:
                set_text.append(line.strip())
    # JSON 형식의 문자열을 딕셔너리로 변환
    setting_list = {}
    if set_text:
        setting_list = json.loads(set_text[0])

    return setting_list

def txtCreate(folder,txt_file,contents):
    # 디렉토리가 없는 경우 생성
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    # 파일 생성
    try:
        with open(folder+'/'+txt_file, "r", encoding="UTF-8") as f:
            pass
    except FileNotFoundError:
        # 파일이 존재하지 않는 경우
        with open(folder+'/'+txt_file, "w", encoding="UTF-8") as f:
            f.write(contents)

def userCkeck(user_id):
    scope = 'https://spreadsheets.google.com/feeds'
    user_json = folder + '/user_ck.json'  # json file path

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(user_json, scope)
    except:
        print("json 파일 없음.(압축파일 다시 풀어서 진행해주세요.)")
        time.sleep(5)
        exit()

    gc = gspread.authorize(credentials)
    sheet_url = 'https://docs.google.com/spreadsheets/d/1o31D_cHjQdNaJ8MUMHu8bkfYmOTN5tvQanxnd5etUeQ/edit#gid=0'  # spreadsheets url
    doc = gc.open_by_url(sheet_url)

    ws = doc.worksheet('program')
    ws_all = ws.get_all_values()
    for i in ws_all:
        if i[2] == user_id:
            user_ck = 1
            break
        else:
            user_ck = 0

    return user_ck

def imgSave(folder,img_file,tag,img_access_key):
    unsplash_url = 'https://api.unsplash.com/'
    headers = {'Authorization': 'Client-ID ' + img_access_key}
    for i in range(0, 5):
        try:
            if i!=4:
                random_page = random.randrange(0,5)
                random_per_page = random.randrange(0, 10)
            else:
                random_page = 1
                random_per_page = 1

            print('이미지 랜덤 돌리기 시도 : ', i + 1)

            para = {'query': tag,'page': random_page, 'per_page': random_per_page, 'lang': 'ko'}  # 이미지 프롬포트 설정
            respons = requests.get(url=unsplash_url + 'search/photos/', params=para, headers=headers)



            url = respons.json()['results'][0]['urls']['regular']
            savelocation = folder + '/' + img_file
            urllib.request.urlretrieve(url, savelocation)  # 이미지 저장
            print('이미지가져오기')
            break
        except:
            pass


    img = cv2.imdecode(np.fromfile(savelocation, dtype=np.uint8), cv2.IMREAD_COLOR)
    # 이미지 썸네일 사이즈 변경
    resized_img = cv2.resize(img, (600, 600))
    # 변경된 이미지 저장
    cv2.imwrite(savelocation, resized_img)

    return savelocation,resized_img

def gtp(prompt,gpt_key,gpt_version):
    # chatgpt api로 블로그 주제와 지시문을 전달하여 글을 생성
    openai.api_key = gpt_key  # chatGPT key

    content = f"""I want you to act as a content writer very proficient SEO Writer. 
                  HTML 형식으로 블로그 게시물을 작성합니다.<body> 태그만 보여주세요.
                  블로그 테마를 "{topic}"로 작성합니다.
                  중요한 단어나 문장을 강조, 굵게 또는 이탤릭체로 표시합니다.
                  다양한 감정적인 언어를 추가하고 비유적인 표현을 사용하여 창의력과 표현력을 풍부하게 작성하세요. 
                  입니다.처럼 다로 끝내지 말고 했어요 같은 요로 끝내주세요. 
                  반복적인 문장이 생기지 않도록 부자연스럽지 않게 작성하세요. 
                  다른 출처의 복사 및 붙여넣기보다는 자신의 말로 기사를 작성하세요.
                  독자의 관심을 끌 수 있는 충분히 상세한 문단을 사용하세요. 
                  사람이 작성한 대로 대화형으로 작성하십시오. 
                  Write a 2000-word 100% Unique, SEO-optimized, Human-Written article with at least 15 headings and subheadings (including H1, H2, H3, and H4 headings) that covers the topic provided in the Prompt.  
                  "Creates multiple hashtags and adds them only to the end of the line."
                """

    print('5~15 분 정도 걸릴 수 있는 점 양해 바랍니다.')

    try:
        # 블로그 생성
        message = [
            {"role": "system", "content": content},
            {"role": "user", "content": prompt}
        ]
        if gpt_version == '3.5-16K':
            model_engine = "gpt-3.5-turbo-16k"  # 모델 엔진 선택
            max_token = 7500

            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=message,
                max_tokens=max_token,
                temperature = 0.3,  # creativity
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0
            )
        elif gpt_version == '4':
            model_engine = "gpt-4-turbo"  # 모델 엔진 선택
            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=message,
                temperature=0.3,  # creativity
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        else:
            print('gpt 버전 에러')
            time.sleep(10)
            exit()

    except Exception as e:
        # 예외가 발생한 경우 예외 메시지를 출력합니다.
        print(f"gpt 에러 : {str(e)}")
        time.sleep(10)
        exit()

    # 응답에서 생성된 텍스트 반환
    return completion['choices'][0]['message']['content']

def gpt_setting_content(content):

    if '<head>' in content:
        blog_write = (content.split('<body>\n')[1]).split('</body>')[0]
    else:
        blog_write = content

    print('blog_write : ', blog_write)

    # 해시태그 추출
    hashtag_pattern = r'(#+[ㄱ-ㅎ가-힣a-zA-Z0-9(_)]{1,})'
    re.findall(hashtag_pattern, blog_write)
    # 해시태그를 태그화 하기 위하여 다음과 같이 문자열 형태로 변경합니다.
    hashtags = [w[1:] for w in re.findall(hashtag_pattern, blog_write)]
    # print('hashtags : ',hashtags)
    tag_string = ""
    # 제목 추출
    real_title = re.search('<h1>(.+?)</h1>', blog_write).group(1)
    for w in hashtags:
        # print('hashtags :',w)
        tag_string += f'{w}, '

    tag_string = re.sub(r'[^ㄱ-ㅎ가-힣a-zA-Z, ]', '', tag_string)

    tag_string = tag_string.strip()[:-1]

    tag = tag_string  # 등록할 태그값, 쉼표로 구분
    print('tag : ', tag)
    # 그림 위치 지정 h1태그 뒤 ,h2태그 두번째 뒤
    h1_step = blog_write.find('</h1>')

    front = blog_write[:h1_step + 5]

    middle = blog_write[h1_step + 5:]

    h2_f_step = middle.find('</h2>')
    middle_front = middle[:h2_f_step + 5]
    middle_mid = middle[h2_f_step + 5:]

    h2_s_step = middle_mid.find('</h2>')
    middle_back = middle_mid[:h2_s_step + 5]
    back = middle_mid[h2_s_step + 5:]

    real_text = front + middle_front + middle_back + back

    return real_text,tag,real_title

def postWriteSelect(blog_id,blog_pw,blog_addr,img_path,category_id,content, tag, real_title, public_ck, delay):
    try:
        subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
    except:
        subprocess.Popen(
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

    url = "https://www.tistory.com/auth/login"

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(), options=option)
    driver.maximize_window()
    driver.get(url)


    if driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/div/a[2]'):
        driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/div/a[2]').click()

        # id
        element = driver.find_element(By.XPATH, '//*[@id="loginId--1"]')
        driver.execute_script("arguments[0].value = '';", element)
        time.sleep(delay)
        element.click()
        element.send_keys(Keys.CONTROL + "a")  # 텍스트 선택
        element.send_keys(Keys.DELETE)  # 선택된 텍스트 삭제
        element.send_keys(blog_id)

        # pw
        element = driver.find_element(By.XPATH, '//*[@id="password--2"]')
        time.sleep(delay)
        element.click()
        element.send_keys(Keys.CONTROL + "a")  # 텍스트 선택
        element.send_keys(Keys.DELETE)  # 선택된 텍스트 삭제
        element.send_keys(blog_pw)

        time.sleep(delay)
        driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

    time.sleep(delay)
    driver.get(blog_addr+'manage/newpost/')
    time.sleep(delay)

    # alert 창 취소
    try:
        driver.switch_to.alert.dismiss()
        time.sleep(delay)
    except:
        pass


    # HTML
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "editor-mode-layer-btn-open"))
    )
    element.click()
    driver.find_element(By.XPATH, '//*[@id="editor-mode-html"]').click()

    # alert 창 확인
    time.sleep(delay)
    try:
        driver.switch_to.alert.accept()
        time.sleep(delay)
    except:
        pass


    #이미지
    if img_path:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="attach-layer-btn"]'))
        )
        element.click()
        time.sleep(delay+2)
        file_input = driver.find_element(By.XPATH, '//*[@id="attach-image"]')
        time.sleep(delay)
        file_input.send_keys(img_path)
        time.sleep(delay)

    # 카테고리
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "category-btn"))
    )
    element.click()

    driver.find_element(By.ID, category_id).click()

    # 제목
    driver.find_element(By.XPATH, '//*[@id="post-title-inp"]').send_keys(real_title)

    # 본문
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="html-editor-container"]/div[2]/div/div/div[6]/div[1]/div/div'))
    )
    element.click()
    driver.find_element(By.XPATH, '//*[@id="html-editor-container"]/div[2]/div/div/div[1]/textarea').send_keys(
        content)
    time.sleep(delay+10)

    # 태그
    driver.find_element(By.XPATH, '//*[@id="tagText"]').send_keys(tag)
    driver.find_element(By.XPATH, '//*[@id="tagText"]').send_keys(Keys.ENTER)
    time.sleep(delay)

    # 완료
    driver.find_element(By.XPATH, '//*[@id="publish-layer-btn"]').click()
    time.sleep(delay)
    if public_ck=='N':
        driver.find_element(By.XPATH, '//*[@id="open0"]').click()
        time.sleep(delay)
    driver.find_element(By.XPATH, '//*[@id="publish-btn"]').click()
    time.sleep(delay)
    driver.close()

    print('자동 포스팅 성공')








# folder = './dist/setting' # dev
folder = './setting' # pro
####################################### 등록 된 유저 확인 #######################################
user_id = txtReading(folder,'login.txt')['user_id']
user_ck = userCkeck(user_id)
print('user ckeck : ',user_id)
if user_ck == 0:
    print('등록되지 않은 이메일입니다. 관리자의 문의하세요')
    time.sleep(5)
    exit()
####################################### 데이터 가져오기 #######################################
topic_count = txtReading(folder, 'topic.txt')
setting = txtReading(folder,'setting.txt')
gpt_prompt = txtReading(folder, 'gpt.txt')['gpt_prompt']
print('반복 횟수 :', setting['count'])
print('총 주제 갯수 :', len(topic_count['topic_list']))

if setting['count'] >= len(topic_count['topic_list']):
    print('반복횟수만큼의 주제가 없습니다.')
    time.sleep(5)
    exit()

for i in range(0,setting['count']):
    print('#######################################' + str(i+1) + '번 시작 #######################################')
    try:
        topic = txtTopic(folder,'topic.txt')

        print('주제 : ',topic)
        ####################################### 이미지 추출 및 사이즈 지정 #######################################
        try:
            img_path, imgsave = imgSave(folder,'1.jpg',topic,setting['img_api'])
            print('img save : okay')
        except:
            img_path=''
            print('img save : 주제에 맞는 img 없음')
        ####################################### gpt 프롬프트 생성 #######################################
        try:
            prompt = gpt_prompt.format(topic=topic)
            print('프롬프트 생성 : okay')
        except:
            print('프롬프트 생성 : gpt 공통 질문 다시 작성해서 프로그램 실행해주세요.')
            time.sleep(5)
            exit()
        ####################################### gpt 프롬프트 생성 #######################################
        response = gtp(prompt,setting['gpt_api'],setting['gpt_version'])
        real_text, tag, real_title = gpt_setting_content(response)

        txtCreate('data/'+'(' + datetime.today().strftime("%Y%m%d") + ')',topic+'(제목)',real_title)
        txtCreate('data/'+'(' + datetime.today().strftime("%Y%m%d") + ')',topic+'(본문)',real_text)
        txtCreate('data/'+'(' + datetime.today().strftime("%Y%m%d") + ')',topic+'(태그)',tag)

        postWriteSelect(setting['blog_id'], setting['blog_pw'], setting['blog_addr'], os.getcwd()+img_path, setting['catagory_list'][setting['catogory_item']], real_text, tag, real_title, setting['public_ck'],setting['net_speed'])

        print('####################################### 반복횟수 : '+ str(i) +' 성공 #######################################')
    except:
        print(i+'번 째 반복 오류')