import streamlit as st #line:1
from selenium import webdriver #line:2
from selenium .webdriver .chrome .options import Options #line:3
from selenium .webdriver .chrome .service import Service #line:4
from selenium .webdriver .support .ui import WebDriverWait #line:5
from selenium .webdriver .support import expected_conditions as EC #line:6
from selenium .webdriver .common .by import By #line:7
from selenium .webdriver .common .keys import Keys #line:8
import gspread #line:9
from oauth2client .service_account import ServiceAccountCredentials #line:10
import json #line:11
import os #line:12
import subprocess #line:13
import time #line:14
import openai #line:15
import re #line:16
import random #line:17
import chromedriver_autoinstaller #line:18
def postWriteSelect (OO00O0OO0OO0O0O0O ,OO0O00O000O0O0O0O ,OOO00OOOOOO00000O ,O00OO0OO0O000O0OO ):#line:20
    chromedriver_autoinstaller .install ()#line:21
    try :#line:22
        subprocess .Popen (r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')#line:24
    except :#line:25
        subprocess .Popen (r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')#line:27
    O0O0000000OOOOOOO ="https://www.tistory.com/auth/login"#line:29
    O00O0OOOOOOO000O0 =Options ()#line:31
    O00O0OOOOOOO000O0 .add_experimental_option ("debuggerAddress","127.0.0.1:9222")#line:32
    O000OO0O0O0OO0O0O =webdriver .Chrome (service =Service (),options =O00O0OOOOOOO000O0 )#line:33
    O000OO0O0O0OO0O0O .maximize_window ()#line:34
    O000OO0O0O0OO0O0O .get (O0O0000000OOOOOOO )#line:35
    if O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="cMain"]/div/div/div/div/a[2]'):#line:37
        O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="cMain"]/div/div/div/div/a[2]').click ()#line:38
        O00O0OO0OOO0OO0O0 =O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="loginId--1"]')#line:41
        O000OO0O0O0OO0O0O .execute_script ("arguments[0].value = '';",O00O0OO0OOO0OO0O0 )#line:42
        time .sleep (O00OO0OO0O000O0OO )#line:43
        O00O0OO0OOO0OO0O0 .click ()#line:44
        O00O0OO0OOO0OO0O0 .send_keys (Keys .CONTROL +"a")#line:45
        O00O0OO0OOO0OO0O0 .send_keys (Keys .DELETE )#line:46
        O00O0OO0OOO0OO0O0 .send_keys (OO00O0OO0OO0O0O0O )#line:47
        O00O0OO0OOO0OO0O0 =O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="password--2"]')#line:50
        time .sleep (O00OO0OO0O000O0OO )#line:51
        O00O0OO0OOO0OO0O0 .click ()#line:52
        O00O0OO0OOO0OO0O0 .send_keys (Keys .CONTROL +"a")#line:53
        O00O0OO0OOO0OO0O0 .send_keys (Keys .DELETE )#line:54
        O00O0OO0OOO0OO0O0 .send_keys (OO0O00O000O0O0O0O )#line:55
        time .sleep (O00OO0OO0O000O0OO )#line:57
        O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click ()#line:58
    time .sleep (O00OO0OO0O000O0OO )#line:60
    O000OO0O0O0OO0O0O .get (OOO00OOOOOO00000O +'manage/newpost/')#line:61
    time .sleep (O00OO0OO0O000O0OO )#line:62
    try :#line:65
        O000OO0O0O0OO0O0O .switch_to .alert .dismiss ()#line:66
    except :#line:67
        pass #line:68
    time .sleep (O00OO0OO0O000O0OO +1 )#line:69
    O00O0OO0OOO0OO0O0 =WebDriverWait (O000OO0O0O0OO0O0O ,10 ).until (EC .presence_of_element_located ((By .ID ,"editor-mode-layer-btn-open")))#line:74
    O00O0OO0OOO0OO0O0 .click ()#line:75
    O000OO0O0O0OO0O0O .find_element (By .XPATH ,'//*[@id="editor-mode-html"]').click ()#line:76
    time .sleep (O00OO0OO0O000O0OO )#line:79
    try :#line:80
        O000OO0O0O0OO0O0O .switch_to .alert .accept ()#line:81
    except :#line:82
        pass #line:83
    time .sleep (O00OO0OO0O000O0OO )#line:84
    O00O0OO0OOO0OO0O0 =WebDriverWait (O000OO0O0O0OO0O0O ,10 ).until (EC .presence_of_element_located ((By .ID ,"category-btn")))#line:89
    O00O0OO0OOO0OO0O0 .click ()#line:90
    O00O0OO0O000OOO00 =O000OO0O0O0OO0O0O .find_element (By .ID ,'category-list')#line:93
    OOOOO00O00OO0O000 =O00O0OO0O000OOO00 .find_elements (By .XPATH ,'.//div[contains(@class, "mce-menu-item")]')#line:96
    print ('categories : ',OOOOO00O00OO0O000 )#line:97
    O00O00OOOO0000000 ={}#line:99
    for OO00000OOO0000O00 in OOOOO00O00OO0O000 :#line:100
        OO00OO0000000OOO0 =OO00000OOO0000O00 .text #line:101
        OOO000OOO0000O00O =OO00000OOO0000O00 .get_attribute ('id')#line:102
        O00O00OOOO0000000 [OO00OO0000000OOO0 ]=OOO000OOO0000O00O #line:103
    O000OO0O0O0OO0O0O .close ()#line:104
    return O00O00OOOO0000000 #line:106
def txtCreateRead (OOOOOOO000OOOO00O ,O000O0000O0OO0OO0 ):#line:108
    try :#line:110
        os .makedirs (OOOOOOO000OOOO00O )#line:111
    except FileExistsError :#line:112
        pass #line:113
    try :#line:115
        with open (OOOOOOO000OOOO00O +'/'+O000O0000O0OO0OO0 ,"r",encoding ="UTF-8")as O00OO00OO0O0O0OO0 :#line:116
            pass #line:117
    except FileNotFoundError :#line:118
        with open (OOOOOOO000OOOO00O +'/'+O000O0000O0OO0OO0 ,"w",encoding ="UTF-8")as O00OO00OO0O0O0OO0 :#line:120
            O00OO00OO0O0O0OO0 .write ("")#line:121
    OO0000OO0OO0OO0O0 =[]#line:124
    if os .path .exists (OOOOOOO000OOOO00O +'/'+O000O0000O0OO0OO0 ):#line:125
        with open (OOOOOOO000OOOO00O +'/'+O000O0000O0OO0OO0 ,"r",encoding ="UTF-8")as O00OO00OO0O0O0OO0 :#line:126
            for OOOO0000000O0OOOO in O00OO00OO0O0O0OO0 :#line:127
                OO0000OO0OO0OO0O0 .append (OOOO0000000O0OOOO .strip ())#line:128
    OOO00O00O0000OO00 ={}#line:131
    if OO0000OO0OO0OO0O0 :#line:132
        OOO00O00O0000OO00 =json .loads (OO0000OO0OO0OO0O0 [0 ])#line:133
    return OOO00O00O0000OO00 #line:135
def saveTxt (O0O000000O000O00O ,OO0O00O000000O0O0 ,O0O0O000OO0OOOOO0 ,is_set =False ,login =False ):#line:137
    if is_set :#line:139
        try :#line:140
            with open (OO0O00O000000O0O0 +"/"+O0O0O000OO0OOOOO0 ,"r",encoding ="UTF-8")as O0O00O00O0O0OOO00 :#line:141
                O0O0OO00O0OOO0000 =json .load (O0O00O00O0O0OOO00 )#line:142
            O0O0OO00O0OOO0000 .update (O0O000000O000O00O )#line:144
        except :#line:145
            O0O0OO00O0OOO0000 =""#line:147
    else :#line:148
        O0O0OO00O0OOO0000 =O0O000000O000O00O #line:149
    with open (OO0O00O000000O0O0 +"/"+O0O0O000OO0OOOOO0 ,"w",encoding ="UTF-8")as O0O00O00O0O0OOO00 :#line:151
        json .dump (O0O0OO00O0OOO0000 ,O0O00O00O0O0OOO00 )#line:152
    if not login :#line:154
        st .success ("저장되었습니다.")#line:155
def gpt (O00OO0OO00OO0OO0O ,OOOOOOOOO00OOO000 ):#line:157
    openai .api_key =O00OO0OO00OO0OO0O #line:159
    try :#line:160
        OOO00O0OOOO00OO0O =[{"role":"system","content":'You are a helpful assistant.'},{"role":"user","content":f'''list 형식에 단어로 대답해줘.다른 설명이나 말은 필요없어. 또한 질문에 맞는 단어 100개 대답해줘. 질문은 {OOOOOOOOO00OOO000}에 관한 질병 이야'''}]#line:165
        O0OOO0OOO000OO0OO =openai .ChatCompletion .create (model ='gpt-3.5-turbo',messages =OOO00O0OOOO00OO0O )#line:169
    except Exception as O00OOOO00O0OO0O0O :#line:170
        print (f"gpt 에러 : {str(O00OOOO00O0OO0O0O)}")#line:172
        return 'N'#line:173
    return O0OOO0OOO000OO0OO #line:176
def user_ck (OOO00OOOOO0O0000O ,O0O00OOO00OOO00OO ):#line:178
    OOO0O00OO0O0OO000 ='https://spreadsheets.google.com/feeds'#line:179
    O0OOO000OOOO0OOOO =OOO00OOOOO0O0000O +'/user_ck.json'#line:180
    try :#line:181
        OOO0OOO00000O0O0O =ServiceAccountCredentials .from_json_keyfile_name (O0OOO000OOOO0OOOO ,OOO0O00OO0O0OO000 )#line:182
    except :#line:183
        st .error ("json 파일 없음.(압축파일 다시 풀어서 진행해주세요.)")#line:184
    O000OO0O0OO00O0OO =gspread .authorize (OOO0OOO00000O0O0O )#line:186
    OO00OO0O0OOOOO000 ='https://docs.google.com/spreadsheets/d/1o31D_cHjQdNaJ8MUMHu8bkfYmOTN5tvQanxnd5etUeQ/edit#gid=0'#line:187
    O00OOO0OO00OO0000 =O000OO0O0OO00O0OO .open_by_url (OO00OO0O0OOOOO000 )#line:188
    O0OOOO0O00OO00000 =O00OOO0OO00OO0000 .worksheet ('program')#line:190
    OOOO0O0OO0OOOOO0O =O0OOOO0O00OO00000 .get_all_values ()#line:191
    for O00O000000OO00OOO in OOOO0O0OO0OOOOO0O :#line:192
        if O00O000000OO00OOO [2 ]==O0O00OOO00OOO00OO :#line:193
            O0000OO0O0O00O0OO =1 #line:194
            st .session_state .vertion =O00O000000OO00OOO [3 ]#line:195
            O000000O000O00O0O ={"user_id":O0O00OOO00OOO00OO }#line:196
            saveTxt (O000000O000O00O0O ,OOO00OOOOO0O0000O ,txt_file ,False ,True )#line:197
            O0O0O0O000OOOO00O =O00OOO0OO00OO0000 .worksheet ('instruction')#line:199
            OOO0OO0OOOOOOOO0O =O0O0O0O000OOOO00O .get_all_values ()#line:200
            for OO0000O0OO0O0OOO0 in OOO0OO0OOOOOOOO0O :#line:202
                if OO0000O0OO0O0OOO0 [1 ]=='AutoTistory'and OO0000O0OO0O0OOO0 [2 ]==O00O000000OO00OOO [3 ]:#line:204
                    st .session_state .AutoTistory_instruction =OO0000O0OO0O0OOO0 [3 ]#line:205
                    break #line:206
            break #line:207
        else :#line:208
            O0000OO0O0O00O0OO =0 #line:209
    return O0000OO0O0O00O0OO #line:211
def setting ():#line:213
    st .title ("AutoTistory Setting")#line:214
    O0OOO00O0O00OO000 ='setting.txt'#line:215
    OOOO0OO0O0O0OOO0O =txtCreateRead (folder ,O0OOO00O0O00OO000 )#line:216
    if 'catagory_list'not in st .session_state :#line:219
        st .session_state .catagory_list =OOOO0OO0O0O0OOO0O .get ("catagory_list","")#line:220
        if 'catagory_list'not in st .session_state :#line:221
            st .session_state .catagory_list =None #line:222
    if 'catogory_item'not in st .session_state :#line:223
        st .session_state .catogory_item =OOOO0OO0O0O0OOO0O .get ("catogory_item","")#line:224
        if 'catogory_item'not in st .session_state :#line:225
            st .session_state .catogory_item =None #line:226
    O00OO00O00O0O0O0O =st .text_input ('블로그 ID (접속할 블로그 ID를 입력해주세요)',value =OOOO0OO0O0O0OOO0O .get ("blog_id","")).strip ()#line:228
    OOO0O000OOOOO0OOO =st .text_input ('블로그 pw (접속할 블로그 pw를 입력해주세요)',type ='password',value =OOOO0OO0O0O0OOO0O .get ("blog_pw","")).strip ()#line:230
    O0OO0O0O000OOOOOO =st .text_input ('Tistory 주소 (접속할 블로그 주소를 입력해주세요)',value =OOOO0OO0O0O0OOO0O .get ("blog_addr","")).strip ()#line:231
    O0OO00000000000O0 ='https://platform.openai.com/account/api-keys'#line:233
    OOO00O000OO0OO0O0 =st .text_input ('GPT API KEY [GPT사이트 바로가기](%s)'%O0OO00000000000O0 ,value =OOOO0OO0O0O0OOO0O .get ("gpt_api","")).strip ()#line:234
    OOO0O0OO000OO00OO ='https://unsplash.com/oauth/applications'#line:236
    OOOO0000OO00O00O0 =st .text_input ('Unsplash API KEY [Unsplash 사이트 바로가기](%s)'%OOO0O0OO000OO00OO ,value =OOOO0OO0O0O0OOO0O .get ("img_api","")).strip ()#line:238
    O0OO0OO00OO0O00O0 =st .slider ("프로그램 동작 횟수",1 ,30 ,OOOO0OO0O0O0OOO0O .get ("count",1 ))#line:240
    O00O0O000OOO0OO0O ={'공개':'Y','비공개':'N'}#line:242
    OO00OO000000O0OOO =list (O00O0O000OOO0OO0O .values ()).index (OOOO0OO0O0O0OOO0O .get ("public_ck","Y"))#line:243
    OOO0OO0O00O0OO0O0 =O00O0O000OOO0OO0O [st .radio ("공개 여부",['공개','비공개'],index =OO00OO000000O0OOO )]#line:244
    OO00OO000000000OO ={'3.5-16K 버전':'3.5-16K','4 버전':'4'}#line:246
    O00O0O00O00O0OOO0 =list (OO00OO000000000OO .values ()).index (OOOO0OO0O0O0OOO0O .get ("gpt_version",'3.5-16K'))#line:247
    O0000O000000000OO =OO00OO000000000OO [st .radio ("GPT 버전",['3.5-16K 버전','4 버전'],index =O00O0O00O00O0OOO0 )]#line:248
    OO000OO0OOO0O0000 ={'엄청 느림':10 ,'느림':8 ,'보통':5 ,'빠름':3 ,'엄청 빠름':1 }#line:250
    OO0O0000O0000O0O0 =list (OO000OO0OOO0O0000 .values ()).index (OOOO0OO0O0O0OOO0O .get ("net_speed",5 ))#line:251
    OO0000OO00OOO000O =OO000OO0OOO0O0000 [st .radio ("네트워크 및 컴퓨터 속도",['엄청 느림','느림','보통','빠름','엄청 빠름'],index =OO0O0000O0000O0O0 )]#line:253
    O000000OO0O00OOOO =st .button ("카테고리 목록 가져오기")#line:256
    OOO00000O00O00O00 ={'1초':1 ,'2초':2 ,'3초':3 ,'4초':4 }#line:258
    O00O00O0O0O00O000 =OOO00000O00O00O00 [st .radio (label ='카테고리 딜레이 (카테고리 버튼 작동안될시 사용)',options =['1초','2초','3초','4초'])]#line:259
    if O000000OO0O00OOOO :#line:261
        if not O00OO00O00O0O0O0O :#line:262
            st .error ("블로그 id를 입력해주세요.")#line:263
        elif not OOO0O000OOOOO0OOO :#line:264
            st .error ("블로그 pw를 입력해주세요.")#line:265
        elif not O0OO0O0O000OOOOOO :#line:266
            st .error ("블로그 주소를 입력해주세요.")#line:267
        else :#line:268
            O0O0O0O00OOOOO000 =postWriteSelect (O00OO00O00O0O0O0O ,OOO0O000OOOOO0OOO ,O0OO0O0O000OOOOOO ,O00O00O0O0O00O000 )#line:269
            st .session_state .catagory_list =O0O0O0O00OOOOO000 #line:270
    if st .session_state .catagory_list :#line:272
        if st .session_state .catogory_item :#line:274
            O0OOO0O0000O00OO0 =list (st .session_state .catagory_list .keys ()).index (st .session_state .catogory_item )#line:275
        else :#line:276
            O0OOO0O0000O00OO0 =0 #line:277
        O000OOOOOO00O0O0O =st .radio ("카테고리 선택",tuple (st .session_state .catagory_list ),index =O0OOO0O0000O00OO0 )#line:279
        st .session_state .catogory_item =O000OOOOOO00O0O0O .strip ()#line:280
    O00O0000OOO0OOO0O =st .button ("저장")#line:283
    if O00O0000OOO0OOO0O :#line:284
        OOO00000OOOOOOOOO ={"blog_id":O00OO00O00O0O0O0O ,"blog_pw":OOO0O000OOOOO0OOO ,"blog_addr":O0OO0O0O000OOOOOO ,"gpt_api":OOO00O000OO0OO0O0 ,"img_api":OOOO0000OO00O00O0 ,"public_ck":OOO0OO0O00O0OO0O0 ,"gpt_version":O0000O000000000OO ,"net_speed":OO0000OO00OOO000O ,"count":O0OO0OO00OO0O00O0 ,"catagory_list":st .session_state .catagory_list ,"catogory_item":st .session_state .catogory_item }#line:298
        saveTxt (OOO00000OOOOOOOOO ,folder ,O0OOO00O0O00OO000 )#line:299
def topic ():#line:301
    st .title ("주제 생성 및 수정")#line:302
    O00O00O0OOO0O0000 ='setting.txt'#line:304
    OOOO000O0OOOO0O0O ='topic.txt'#line:305
    OOO0O000OOO000O0O =txtCreateRead (folder ,O00O00O0OOO0O0000 )#line:307
    O0O00000OOO000OO0 =txtCreateRead (folder ,OOOO000O0OOOO0O0O )#line:308
    OO00OOOOO000000O0 ={'자동 생성':'auto','수동 생성 및 변경':'not auto'}#line:310
    OOO0OO0O0O00O0O0O =list (OO00OOOOO000000O0 .values ()).index (O0O00000OOO000OO0 .get ("tistory_topic",'not auto'))#line:311
    st .session_state .tistory_topic =OO00OOOOO000000O0 [st .radio ("티스토리 주제",['자동 생성','수동 생성 및 변경'],index =OOO0OO0O0O00O0O0O )]#line:313
    if st .session_state .tistory_topic =='auto':#line:315
        OOOO0OO0O000OOOOO =st .text_input ('카테고리 작성 (특수문자 사용X)')#line:316
        O0OO0000O0OO0OO00 =st .button ('카테고리에 맞는 주제 생성')#line:317
        if O0OO0000O0OO0OO00 :#line:318
            for O0O0OO0O000000OOO in range (3 ):#line:319
                OOOOO00O0OO0OOOO0 =gpt (OOO0O000OOO000O0O .get ('gpt_api'),OOOO0OO0O000OOOOO )#line:320
                try :#line:322
                    st .session_state .topic_list =[OO00O00O000OOOOOO .strip ("' ")for OO00O00O000OOOOOO in OOOOO00O0OO0OOOO0 ['choices'][0 ]['message']['content'].split (",")]#line:325
                    print (st .session_state .topic_list )#line:326
                    st .session_state .topic_list =[re .sub (r'^\d+\.','',OOOOOO00OOOO0OO00 .strip ()).strip ()for OOOOOO00OOOO0OO00 in OOOOO00O0OO0OOOO0 ['choices'][0 ]['message']['content'].split ('\n')]#line:328
                    print (st .session_state .topic_list )#line:329
                    st .text_area (OOOO0OO0O000OOOOO +'관한 주제 100개','\n'.join (st .session_state .topic_list ),height =1000 )#line:335
                    break ;#line:336
                except :#line:337
                    print ('brr : ',O0O0OO0O000000OOO )#line:338
                    if O0O0OO0O000000OOO ==2 :#line:339
                        break ;#line:340
    elif st .session_state .tistory_topic =='not auto':#line:342
        O00OOOOOO0O00000O =''#line:343
        for O000OO0OO0000O00O ,O0O00O0O00O0O00O0 in enumerate (O0O00000OOO000OO0 .get ("topic_list",[]),start =1 ):#line:344
            O00OOOOOO0O00000O +=O0O00O0O00O0O00O0 +'\n'#line:345
        O00OOOOOO0O00000O =O00OOOOOO0O00000O .rstrip ('\n')#line:347
        st .session_state .topic_list =st .text_area ('주제를 한줄씩 작성하세요(특수문자 사용X)',O00OOOOOO0O00000O ,height =200 ).split ("\n")#line:352
    if 'topic_list'not in st .session_state :#line:354
        st .session_state .topic_list =None #line:355
    OO0O0000OO0OO00OO =st .button ("저장")#line:357
    if OO0O0000OO0OO00OO :#line:358
        if st .session_state .topic_list :#line:359
            saveTxt ({'topic_list':st .session_state .topic_list },folder ,OOOO000O0OOOO0O0O )#line:361
def topicList ():#line:363
    O0O000O0O0O000OOO ='topic.txt'#line:364
    OOO00OO00OO0OO00O =txtCreateRead (folder ,O0O000O0O0O000OOO )#line:365
    st .write ('저장된 주제')#line:366
    st .write (OOO00OO00OO0OO00O .get ("topic_list",'저장된 주제가 없습니다.'))#line:367
def gptprompt ():#line:369
    st .title ("GPT 공통 질문")#line:370
    OO0OO000O00O0O0OO ='topic.txt'#line:372
    O0O0OOO0OO0OOOO00 ='gpt.txt'#line:373
    O00OOOOOO00OOOO0O =txtCreateRead (folder ,OO0OO000O00O0O0OO )#line:375
    OOOO00000O0OOOOOO =txtCreateRead (folder ,O0O0OOO0OO0OOOO00 )#line:376
    st .session_state .gpt_prompt =st .text_area ("GPT 공통 질문 생성 ([질문예시](%s)"%'https://www.notion.so/GPT-4ffaf3652cbc49a3b978a2cb6d9b29e1'+")",OOOO00000O0OOOOOO .get ('gpt_prompt',''),height =300 )#line:380
    O0OOOOOOOO0OO00OO =st .button ("질문 확인")#line:381
    if O0OOOOOOOO0OO00OO :#line:383
        try :#line:384
            st .write ('GPT 공통 질문 확인')#line:385
            OOO0000O0O0OO0000 =random .randint (1 ,len (O00OOOOOO00OOOO0O .get ('topic_list')))#line:386
            st .success (st .session_state .gpt_prompt .format (topic =O00OOOOOO00OOOO0O .get ('topic_list')[OOO0000O0O0OO0000 ]))#line:387
        except :#line:388
            st .error ('gpt 양식을 확인해 다시 작성해주세요.')#line:389
    OO000OOOOO0OOO00O =st .button ("저장")#line:390
    if OO000OOOOO0OOO00O :#line:392
        O0O00OO0000OOO000 ={"gpt_prompt":st .session_state .gpt_prompt }#line:394
        saveTxt (O0O00OO0000OOO000 ,folder ,O0O0OOO0OO0OOOO00 )#line:395
        st .success ('셋팅을 다하셨다면 프로그램을 닫으시고, main.exe 프로그램을 실행시켜 주세요.')#line:396
st .write ('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',unsafe_allow_html =True )#line:398
folder ='./setting'#line:400
if 'user_ck'not in st .session_state :#line:404
    st .session_state .user_ck =None #line:405
if st .session_state .user_ck !=1 :#line:407
    txt_file ='login.txt'#line:408
    setting_list =txtCreateRead (folder ,txt_file )#line:409
    st .title ("AutoTistory Login")#line:411
    user_id =st .text_input ("귀자개(개발자)님한테 전달한 이메일 주소를 작성하세요 ([사용방법](%s)"%"https://fate-dart-576.notion.site/AutoTistory-V4-9c2b1cf473cf44b4a0b1448b3b814a92?pvs=4"+")",value =setting_list .get ("user_id",""))#line:412
    st .write ("개발자 문의는 [여기](%s)"%'https://open.kakao.com/o/sjxp87Af'+"로 주세요. (문의 주실때 닉네임은 이메일로 부탁드립니다.)")#line:413
    button_login =st .button ("로그인")#line:415
    if button_login :#line:417
        st .session_state .user_ck =user_ck (folder ,user_id )#line:418
if st .session_state .user_ck ==1 :#line:420
    if 'sidebar'not in st .session_state :#line:422
        st .session_state .sidebar =None #line:423
    st .sidebar .title ('AutoTistory')#line:425
    if st .sidebar .button ('AutoTistory Setting'):#line:426
        st .session_state .sidebar ='AutoTistory Setting'#line:427
    if st .sidebar .button ('주제 생성 및 수정'):#line:428
        st .session_state .sidebar ='주제 생성 및 수정'#line:429
    if st .sidebar .button ('저장된 주제'):#line:430
        st .session_state .sidebar ='저장된 주제'#line:431
    if st .sidebar .button ('GPT 공통 질문'):#line:432
        st .session_state .sidebar ='GPT 공통 질문'#line:433
    if st .sidebar .button ('사용 설명서'):#line:434
        st .session_state .sidebar ='사용 설명서'#line:435
    if st .session_state .sidebar =='AutoTistory Setting':#line:437
        setting ()#line:438
    elif st .session_state .sidebar =='주제 생성 및 수정':#line:440
        topic ()#line:441
    elif st .session_state .sidebar =='저장된 주제':#line:443
        topicList ()#line:444
    elif st .session_state .sidebar =='GPT 공통 질문':#line:446
        gptprompt ()#line:447
    elif st .session_state .sidebar =='사용 설명서':#line:448
        st .write ("1. [사용 설명서](%s)"%"https://fate-dart-576.notion.site/AutoTistory-V4-9c2b1cf473cf44b4a0b1448b3b814a92?pvs=4")#line:449
        st .write ("2. [개발자 문의](%s)"%'https://open.kakao.com/o/sjxp87Af'+" (문의 주실때 닉네임은 이메일로 부탁드립니다.)")#line:450
    else :#line:451
        st .success (user_id +"님 반갑습니다 \n 고객님이 사용하시는 버전은 "+st .session_state .vertion +" 입니다. \n 메뉴를 선택해주세요.")#line:452
elif st .session_state .user_ck ==0 :#line:453
    st .error ("등록되지 않은 이메일입니다. 관리자의 문의하세요.")#line:454
