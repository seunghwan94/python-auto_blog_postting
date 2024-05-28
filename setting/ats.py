import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import subprocess
import time
import openai
import re
import random
import chromedriver_autoinstaller

def postWriteSelect(id,pw,redirect_uri,delay):
    chromedriver_autoinstaller.install()
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

    if driver.find_element(By.XPATH, '//*[@id="cMain"]/div/div/div/a[2]'):
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/a[2]').click()

        # id
        element = driver.find_element(By.XPATH, '//*[@id="loginId--1"]')
        driver.execute_script("arguments[0].value = '';", element)
        time.sleep(delay)
        element.click()
        element.send_keys(Keys.CONTROL + "a")  # 텍스트 선택
        element.send_keys(Keys.DELETE)  # 선택된 텍스트 삭제
        element.send_keys(id)

        # pw
        element = driver.find_element(By.XPATH, '//*[@id="password--2"]')
        time.sleep(delay)
        element.click()
        element.send_keys(Keys.CONTROL + "a")  # 텍스트 선택
        element.send_keys(Keys.DELETE)  # 선택된 텍스트 삭제
        element.send_keys(pw)

        time.sleep(delay)
        driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()

    time.sleep(delay)
    driver.get(redirect_uri+'manage/newpost/')
    time.sleep(delay)

    # alert 창 취소
    try:
        driver.switch_to.alert.dismiss()
    except:
        pass
    time.sleep(delay+1)

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
    except:
        pass
    time.sleep(delay)

    # 카테고리
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "category-btn"))
    )
    element.click()

    # "category-list" div 요소 찾기
    category_list = driver.find_element(By.ID,'category-list')

    # 하위 요소들 찾기
    categories = category_list.find_elements(By.XPATH,'.//div[contains(@class, "mce-menu-item")]')
    print('categories : ',categories)
    # 각 카테고리 텍스트 추출 및 출력
    category_array = {}
    for category in categories:
        category_text = category.text
        category_id = category.get_attribute('id')
        category_array[category_text] = category_id
    driver.close()

    return category_array

def txtCreateRead(folder,txt_file):
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
            f.write("")

    # 파일 읽기
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

def saveTxt(key_value,folder,txt_file,is_set=False,login=False):
    # 기존 데이터 불러오기
    if is_set:
        try:
            with open(folder + "/" + txt_file, "r", encoding="UTF-8") as f:
                existing_data = json.load(f)
            # 새로운 키-값 쌍 추가
            existing_data.update(key_value)
        except:
            # 공백일 경우
            existing_data = ""
    else:
        existing_data = key_value
    # 수정된 데이터를 파일에 저장
    with open(folder + "/" + txt_file, "w", encoding="UTF-8") as f:
        json.dump(existing_data, f)

    if not login:
        st.success("저장되었습니다.")

def gpt(gpt_key,input_topic):
    # chatgpt api로 블로그 주제와 지시문을 전달하여 글을 생성
    openai.api_key = gpt_key  # chatGPT key
    try:
        # 블로그 생성
        message = [
            {"role": "system", "content": 'You are a helpful assistant.'},
            {"role": "user", "content": f'''list 형식에 단어로 대답해줘.다른 설명이나 말은 필요없어. 또한 질문에 맞는 단어 100개 대답해줘. 질문은 {input_topic}에 관한 질병 이야'''}
        ]
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=message
        )
    except Exception as e:
        # 예외가 발생한 경우 예외 메시지를 출력합니다.
        print(f"gpt 에러 : {str(e)}")
        return 'N'

    # 응답에서 생성된 텍스트 반환
    return completion

def user_ck(folder,user_id):
    scope = 'https://spreadsheets.google.com/feeds'
    user_json = folder + '/user_ck.json'  # json file path
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(user_json, scope)
    except:
        st.error("json 파일 없음.(압축파일 다시 풀어서 진행해주세요.)")

    gc = gspread.authorize(credentials)
    sheet_url = 'https://docs.google.com/spreadsheets/d/1o31D_cHjQdNaJ8MUMHu8bkfYmOTN5tvQanxnd5etUeQ/edit#gid=0'  # spreadsheets url
    doc = gc.open_by_url(sheet_url)

    ws_p = doc.worksheet('program')
    ws_p_all = ws_p.get_all_values()
    for p in ws_p_all:
        if p[2] == user_id:
            user_ck = 1
            st.session_state.vertion = p[3]
            user_id_info = {"user_id": user_id}
            saveTxt(user_id_info, folder, txt_file, False, True)

            ws_i = doc.worksheet('instruction')
            ws_i_all = ws_i.get_all_values()

            for i in ws_i_all:
                # 프로그램 이름 및 버전 확인 후 설명서 추출
                if i[1] == 'AutoTistory' and i[2] == p[3]:
                    st.session_state.AutoTistory_instruction = i[3]
                    break
            break
        else:
            user_ck = 0

    return user_ck

def setting():
    st.title("AutoTistory Setting")
    txt_file = 'setting.txt'
    setting_list = txtCreateRead(folder, txt_file)

    # session state 값 확인
    if 'catagory_list' not in st.session_state:
        st.session_state.catagory_list = setting_list.get("catagory_list", "")
        if 'catagory_list' not in st.session_state:
            st.session_state.catagory_list = None
    if 'catogory_item' not in st.session_state:
        st.session_state.catogory_item = setting_list.get("catogory_item", "")
        if 'catogory_item' not in st.session_state:
            st.session_state.catogory_item = None

    blog_id = st.text_input('블로그 ID (접속할 블로그 ID를 입력해주세요)', value=setting_list.get("blog_id", "")).strip()
    blog_pw = st.text_input('블로그 pw (접속할 블로그 pw를 입력해주세요)', type='password',
                            value=setting_list.get("blog_pw", "")).strip()
    blog_addr = st.text_input('Tistory 주소 (접속할 블로그 주소를 입력해주세요)', value=setting_list.get("blog_addr", "")).strip()

    gpt_url = 'https://platform.openai.com/account/api-keys'
    gpt_api = st.text_input('GPT API KEY [GPT사이트 바로가기](%s)' % gpt_url, value=setting_list.get("gpt_api", "")).strip()

    img_url = 'https://unsplash.com/oauth/applications'
    img_api = st.text_input('Unsplash API KEY [Unsplash 사이트 바로가기](%s)' % img_url,
                            value=setting_list.get("img_api", "")).strip()

    count = st.slider("프로그램 동작 횟수", 1, 30, setting_list.get("count", 1))

    public_mapping = {'공개': 'Y', '비공개': 'N'}
    default_public = list(public_mapping.values()).index(setting_list.get("public_ck", "Y"))
    public_ck = public_mapping[st.radio("공개 여부", ['공개', '비공개'], index=default_public)]

    gpt_mapping = {'3.5-16K 버전': '3.5-16K', '4 버전': '4'}
    default_gpt = list(gpt_mapping.values()).index(setting_list.get("gpt_version", '3.5-16K'))
    gpt_version = gpt_mapping[st.radio("GPT 버전", ['3.5-16K 버전', '4 버전'], index=default_gpt)]

    net_speed_mapping = {'엄청 느림': 10, '느림': 8, '보통': 5, '빠름': 3, '엄청 빠름': 1}
    default_net_speed = list(net_speed_mapping.values()).index(setting_list.get("net_speed", 5))
    net_speed = net_speed_mapping[
        st.radio("네트워크 및 컴퓨터 속도", ['엄청 느림', '느림', '보통', '빠름', '엄청 빠름'], index=default_net_speed)]

    # 카테고리 목록 가져오기 버튼
    button_clicked = st.button("카테고리 목록 가져오기")
    # 딜레이 체크박스
    delay_mapping = {'1초': 1, '2초': 2, '3초': 3, '4초': 4}
    delay = delay_mapping[st.radio(label='카테고리 딜레이 (카테고리 버튼 작동안될시 사용)', options=['1초', '2초', '3초', '4초'])]
    # 카테고리 목록
    if button_clicked:
        if not blog_id:
            st.error("블로그 id를 입력해주세요.")
        elif not blog_pw:
            st.error("블로그 pw를 입력해주세요.")
        elif not blog_addr:
            st.error("블로그 주소를 입력해주세요.")
        else:
            catagory_list = postWriteSelect(blog_id, blog_pw, blog_addr, delay)
            st.session_state.catagory_list = catagory_list
    # 카테고리 선택
    if st.session_state.catagory_list:

        if st.session_state.catogory_item:
            index_cat = list(st.session_state.catagory_list.keys()).index(st.session_state.catogory_item)
        else:
            index_cat = 0

        catogory_item = st.radio("카테고리 선택", tuple(st.session_state.catagory_list), index=index_cat)
        st.session_state.catogory_item = catogory_item.strip()
    # Display the selected item

    button_save = st.button("저장")
    if button_save:
        # 입력 받은 정보를 딕셔너리로 저장
        blog_info = {
            "blog_id": blog_id,
            "blog_pw": blog_pw,
            "blog_addr": blog_addr,
            "gpt_api": gpt_api,
            "img_api": img_api,
            "public_ck": public_ck,
            "gpt_version": gpt_version,
            "net_speed": net_speed,
            "count": count,
            "catagory_list": st.session_state.catagory_list,
            "catogory_item": st.session_state.catogory_item
        }
        saveTxt(blog_info, folder, txt_file)

def topic():
    st.title("주제 생성 및 수정")

    txt_file_setting = 'setting.txt'
    txt_file = 'topic.txt'

    setting_list_setting = txtCreateRead(folder, txt_file_setting)
    setting_list = txtCreateRead(folder, txt_file)

    tistory_topic_mapping = {'자동 생성': 'auto', '수동 생성 및 변경': 'not auto'}
    default_tistory_topic = list(tistory_topic_mapping.values()).index(setting_list.get("tistory_topic", 'not auto'))
    st.session_state.tistory_topic = tistory_topic_mapping[
        st.radio("티스토리 주제", ['자동 생성', '수동 생성 및 변경'], index=default_tistory_topic)]

    if st.session_state.tistory_topic == 'auto':
        input_topic = st.text_input('카테고리 작성 (특수문자 사용X)')
        button_topic = st.button('카테고리에 맞는 주제 생성')
        if button_topic:
            for i in range(3):
                response = gpt(setting_list_setting.get('gpt_api'), input_topic)

                try:

                    st.session_state.topic_list = [item.strip("' ") for item in
                                                   response['choices'][0]['message']['content'].split(",")]
                    print(st.session_state.topic_list)
                    st.session_state.topic_list = [re.sub(r'^\d+\.', '', line.strip()).strip() for line in
                                                   response['choices'][0]['message']['content'].split('\n')]
                    print(st.session_state.topic_list)

                    st.text_area(
                        input_topic + '관한 주제 100개',
                        '\n'.join(st.session_state.topic_list),
                        height=1000
                    )
                    break;
                except:
                    print('brr : ', i)
                    if i == 2:
                        break;

    elif st.session_state.tistory_topic == 'not auto':
        txt = ''
        for index, value in enumerate(setting_list.get("topic_list", []), start=1):
            txt += value + '\n'

        txt = txt.rstrip('\n')

        st.session_state.topic_list = st.text_area(
            '주제를 한줄씩 작성하세요(특수문자 사용X)',
            txt,
            height=200).split("\n")

    if 'topic_list' not in st.session_state:
        st.session_state.topic_list = None

    button_save = st.button("저장")
    if button_save:
        if st.session_state.topic_list:
            # st.session_state.topic_list = [re.sub(r'^\d+\.', '', line.strip()).strip() for line in st.session_state.topic_list.split('\n')]
            saveTxt({'topic_list': st.session_state.topic_list}, folder, txt_file)

def topicList():
    txt_file = 'topic.txt'
    setting_topic_list = txtCreateRead(folder, txt_file)
    st.write('저장된 주제')
    st.write(setting_topic_list.get("topic_list", '저장된 주제가 없습니다.'))

def gptprompt():
    st.title("GPT 공통 질문")

    txt_file_topic = 'topic.txt'
    txt_file = 'gpt.txt'

    setting_list_topic = txtCreateRead(folder, txt_file_topic)
    setting_list = txtCreateRead(folder, txt_file)

    st.session_state.gpt_prompt = st.text_area(
        "GPT 공통 질문 생성 ([질문예시](%s)" % 'https://www.notion.so/GPT-4ffaf3652cbc49a3b978a2cb6d9b29e1' + ")",
        setting_list.get('gpt_prompt', ''), height=300)
    button_test = st.button("질문 확인")

    if button_test:
        try:
            st.write('GPT 공통 질문 확인')
            gpt_random = random.randint(1, len(setting_list_topic.get('topic_list')))  # 주제 랜덤으로 가져와서 확인
            st.success(st.session_state.gpt_prompt.format(topic=setting_list_topic.get('topic_list')[gpt_random]))
        except:
            st.error('gpt 양식을 확인해 다시 작성해주세요.')
    button_save = st.button("저장")

    if button_save:
        # 입력 받은 정보를 딕셔너리로 저장
        gpt_prompt_info = {"gpt_prompt": st.session_state.gpt_prompt}
        saveTxt(gpt_prompt_info, folder, txt_file)
        st.success('셋팅을 다하셨다면 프로그램을 닫으시고, main.exe 프로그램을 실행시켜 주세요.')

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

folder = './setting'


###################################### 등록 된 유저 확인 #######################################
if 'user_ck' not in st.session_state:
    st.session_state.user_ck = None

if st.session_state.user_ck!=1:
    txt_file = 'login.txt'
    setting_list = txtCreateRead(folder, txt_file)

    st.title("AutoTistory Login")
    user_id = st.text_input("귀자개(개발자)님한테 전달한 이메일 주소를 작성하세요 ([사용방법](%s)" % "https://fate-dart-576.notion.site/AutoTistory-V4-9c2b1cf473cf44b4a0b1448b3b814a92?pvs=4"+")", value=setting_list.get("user_id", ""))
    st.write("개발자 문의는 [여기](%s)" % 'https://open.kakao.com/o/sjxp87Af' + "로 주세요. (문의 주실때 닉네임은 이메일로 부탁드립니다.)")

    button_login = st.button("로그인")

    if button_login:
        st.session_state.user_ck = user_ck(folder,user_id)
###################################### 등록 된 유저 끝 #######################################
if st.session_state.user_ck==1:
    # 세션 상태에 selected_option 저장
    if 'sidebar' not in st.session_state:
        st.session_state.sidebar = None
    # sidebar
    st.sidebar.title('AutoTistory')
    if st.sidebar.button('AutoTistory Setting'):
        st.session_state.sidebar = 'AutoTistory Setting'
    if st.sidebar.button('주제 생성 및 수정'):
        st.session_state.sidebar = '주제 생성 및 수정'
    if st.sidebar.button('저장된 주제'):
        st.session_state.sidebar = '저장된 주제'
    if st.sidebar.button('GPT 공통 질문'):
        st.session_state.sidebar = 'GPT 공통 질문'
    if st.sidebar.button('사용 설명서'):
        st.session_state.sidebar = '사용 설명서'
###################################### AutoTistory_main_Setting page ######################################
    if st.session_state.sidebar == 'AutoTistory Setting':
        setting()
###################################### AutoTistory_sub_Setting page ######################################
    elif st.session_state.sidebar == '주제 생성 및 수정':
        topic()
###################################### 저장된 주제 page ######################################
    elif st.session_state.sidebar == '저장된 주제':
        topicList()
###################################### GPT 질문 page ######################################
    elif st.session_state.sidebar == 'GPT 공통 질문':
        gptprompt()
    elif st.session_state.sidebar == '사용 설명서':
        st.write("1. [사용 설명서](%s)" % "https://fate-dart-576.notion.site/AutoTistory-V4-9c2b1cf473cf44b4a0b1448b3b814a92?pvs=4")
        st.write("2. [개발자 문의](%s)" % 'https://open.kakao.com/o/sjxp87Af' + " (문의 주실때 닉네임은 이메일로 부탁드립니다.)")
    else:
        st.success(user_id+"님 반갑습니다 \n 고객님이 사용하시는 버전은 "+st.session_state.vertion+" 입니다. \n 메뉴를 선택해주세요.")
elif st.session_state.user_ck==0:
    st.error("등록되지 않은 이메일입니다. 관리자의 문의하세요.")



