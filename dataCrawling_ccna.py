from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
import numpy as np
import dbManagement.DbManagement as db
import numpy as np
import pandas as pd

wrong_answer = []
exam = []
answer = []
question = []

path_to_extension = r'C:\Users\User\Desktop\3.10.2_0'
option = Options()

option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)

driver = webdriver.Chrome()
driver.get("https://itexamanswers.net/ccna-1-v7-exam-answers-introduction-to-networks-v7-0-itn.html/")
time.sleep(1)
driver.implicitly_wait(10)

element = driver.find_element_by_xpath(
    '/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/table[1]/tbody/tr[3]/td[2]/a')
time.sleep(1)
element.click()
driver.implicitly_wait(10)

element = driver.find_element_by_xpath(
    '/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[12]/div/input[3]')
time.sleep(1)
element.click()
driver.implicitly_wait(10)

element = driver.find_element_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[2]/input')
time.sleep(1)
element.click()
driver.implicitly_wait(10)

element = driver.find_element_by_xpath(
    '/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[9]/div[4]/input[2]')
time.sleep(1)
element.click()
driver.implicitly_wait(10)

elements = driver.find_elements_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[12]/ol/li')

count = 0
for i in range(1, len(elements)+1):
    wrong_answer.append([])
    answer.append([])
    exam.append(driver.find_element_by_css_selector(f'#wpProQuiz_299 > div.wpProQuiz_quiz > ol > li:nth-child({i}) > div.wpProQuiz_question > div').text)
    total_answer = driver.find_elements_by_css_selector(f'#wpProQuiz_299 > div.wpProQuiz_quiz > ol > li:nth-child({i}) > div.wpProQuiz_question > ul > li')
    for j in range(0, len(total_answer)):
        get_class = total_answer[j].get_attribute('class')
        if get_class == 'wpProQuiz_questionListItem':
            wrong_answer[count].append(total_answer[j].text)
        else:
            answer[count].append(total_answer[j].text)
    count+=1

for i in range(len(exam)):
    p = re.compile('^[Match|Refer|Open]', flags=re.MULTILINE)
    try:
        temp = exam[i]
        m = p.match(temp)
        if m:
            exam.pop(i)
            wrong_answer.pop(i)
            answer.pop(i)
    except:
        break # 이미지 문제 제거 작업(1)

for i in range(len(wrong_answer)):
    p = re.compile('^[\d.*]')
    try:
        temp = wrong_answer[i][0]
        m = p.match(temp)
        if m:
            continue
        else:
            answer.pop(i)
            exam.pop(i)
            wrong_answer.pop(i)
    except:
        break # 이미지 문제 제거 작업(2)

for i in range(len(wrong_answer)):
    for j in range(len(wrong_answer[i])):
        temp = str(wrong_answer[i][j])
        temp = re.sub('^[\d.*]','',temp)
        wrong_answer[i][j] = temp[2:]

for i in range(len(answer)):
    for j in range(len(answer[i])):
        temp = str(answer[i][j])
        temp = re.sub('^[\d.*]','',temp)
        answer[i][j] = temp[2:]


question.append(exam)
question.append(wrong_answer)
question.append(answer)

question_np = np.array(question, dtype=object)

question_list = {"exam": [question[0]], "wrong_answer": [question[1]], "answer": [question[2]]}
question_pd = pd.DataFrame(question_list)
question_pd.to_csv("./question.csv")
ccna_1_3 = db.Question(exam, wrong_answer, answer)
ccna_1_3.writeCSV('hi.csv')
ccna_1_3.insertDB('hi.csv')