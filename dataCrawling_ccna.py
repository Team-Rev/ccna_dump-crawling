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

main_category = ''
sub_category = ''

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

main_category = driver.find_element_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/p[2]/a/strong').text

element = driver.find_element_by_xpath(
    '/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/table[1]/tbody/tr[5]/td[2]/a')
sub_category = driver.find_element_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/table[1]/tbody/tr[5]/td[1]/a').text

print(main_category)
print(sub_category)
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
bias = 1
cnt = 0
for i in elements:
    wrong_answer.append([])
    answer.append([])
    exam_text = i.find_element_by_class_name('wpProQuiz_question_text').text

    answer_path = driver.find_elements_by_xpath(
        f'/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[12]/ol/li[{bias}]/div[3]/ul/li')
    for j in answer_path:
        get_class = j.get_attribute('class')
        if get_class == 'wpProQuiz_questionListItem':
            wrong_answer[cnt].append(j.text)
        else:
            answer[cnt].append(j.text)
    try:
        i.find_element_by_xpath('.//img')
        continue
    except:
        p = re.compile('^[Match|Open]', flags=re.MULTILINE)
        p2 = re.compile('^[Refer]', flags=re.MULTILINE)
        # p2 = re.compile('^[Refer]', flags=re.MULTILINE)
        m = p.match(exam_text)
        m2 = p2.match(exam_text)
        if m:
            wrong_answer.pop(cnt)
            answer.pop(cnt)

        elif m2:
            pointer = str(exam_text).find('\n')
            if pointer < 0:
                wrong_answer.pop(cnt)
                answer.pop(cnt)
            else:
                exam.append(exam_text)
        else:
            exam.append(exam_text)
    cnt += 1
    bias += 1

            # for j in answer_path:
            #     get_class = answer_path[j].get_attribute('class')
            #     if get_class == 'wpProQuiz_questionListItem':
            #         wrong_answer[i].append(j.text)
            #     else:
            #         answer[i].append(j.text)

# for i in range(len(elements)):
#     try:
#         p = re.compile('^[Match|Open]', flags=re.MULTILINE)
#         temp = elements[i].find_element_by_class_name('wpProQuiz_question_text').text
#         m = p.match(temp)
#         if m:
#             elements.pop(i)
#             wrong_answer.pop(i)
#             answer.pop(i)
#        # elements[i].find_element_by_xpath('.//img')
#        #  elements.pop(i)
#        #  wrong_answer.pop(i)
#        #  answer.pop(i)
#     except:
#         continue

# for i in range(len(exam)):
#     p = re.compile('^[Match|Open]', flags=re.MULTILINE)
#     try:
#         temp = exam[i]
#         m = p.match(temp)
#         if m:
#             exam.pop(i)
#             wrong_answer.pop(i)
#             answer.pop(i)
#     except:
#         continue # 이미지 문제 제거 작업(1)

question.append(exam)
question.append(wrong_answer)
question.append(answer)

sub_category = sub_category.split(':')[0]
question_name = f'{sub_category}_question.csv'
wrong_name = f'{sub_category}_wrong.csv'
right_name = f'{sub_category}_right.csv'

for i in range(len(exam)):
    pointer = str(exam[i]).find("\n")
    if pointer > 0:
        main_exam = ''
        splited_exam = str(exam[i]).split("\n")
        main_exam = splited_exam[0]
        splited_exam = splited_exam[1:]
        prompt_exam = ''

        for j in range(len(splited_exam)):
            prompt_exam = prompt_exam+'</br>'+str(splited_exam[j])
        prompt_exam = prompt_exam[5:]
        prompt_exam = '<prompt>'+str(prompt_exam)+'</prompt>'
        exam[i] = main_exam+prompt_exam



#
ccna_1_3 = db.Question(exam, main_category, sub_category, wrong_answer, answer)
ccna_1_3.write_question_CSV(question_name)
ccna_1_3.write_wrong_choice_CSV(wrong_name)
ccna_1_3.write_right_choice_CSV(right_name)

#
# ccna_1_3.insert_question_DB('Modules 8 – 10_question.csv')
# ccna_1_3.insert_choice_DB('Modules 8 – 10_wrong.csv')
# ccna_1_3.insert_choice_DB('Modules 8 – 10_right.csv')