from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import re
import dbManagement.DbManagement as db

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
driver.get("https://itexamanswers.net/ccna-2-v7-exam-answers-switching-routing-and-wireless-essentials-v7-0-srwe.html")
time.sleep(1)
driver.implicitly_wait(10)

main_category = driver.find_element_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/p[2]/a/strong').text

element = driver.find_element_by_xpath(
    '/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/table[1]/tbody/tr[4]/td[2]/a')
sub_category = driver.find_element_by_xpath('/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/table[1]/tbody/tr[4]/td[1]/a').text

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
    print(bias)
    exam_text = i.find_element_by_class_name('wpProQuiz_question_text').text
    answer_path = driver.find_elements_by_xpath(
        f'/html/body/div[1]/div/article/div/div[1]/div/div/div[3]/div[2]/div[12]/ol/li[{bias}]/div[3]/ul/li')
    p = re.compile('^\d[.].', flags=re.MULTILINE)
    m = p.match(answer_path[0].text)
    if m:
        wrong_answer.append([])
        answer.append([])
        for j in answer_path:
            del_num = str(j.text).find('.')
            choice = str(j.text)[del_num + 2:]
            get_class = j.get_attribute('class')
            if get_class == 'wpProQuiz_questionListItem':
                wrong_answer[cnt].append(choice)
            else:
                answer[cnt].append(choice)
    else:
        bias += 1
        continue
    try:
        i.find_element_by_xpath('.//img')
        wrong_answer.pop(cnt)
        answer.pop(cnt)
        bias += 1
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
            cnt -= 1

        elif m2:
            pointer = str(exam_text).find('\n')
            if pointer < 0:
                wrong_answer.pop(cnt)
                answer.pop(cnt)
                cnt -= 1
            else:
                exam.append(exam_text)
        else:
            exam.append(exam_text)
    cnt += 1
    bias += 1

question.append(exam)
question.append(wrong_answer)
question.append(answer)

sub_category = sub_category.split(':')[0]
question_name = f"{main_category.replace(' ','')}_{sub_category}_question.csv"
wrong_name = f"{main_category.replace(' ','')}_{sub_category}_wrong.csv"
right_name = f"{main_category.replace(' ','')}_{sub_category}_right.csv"

cnt = 0


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
# ccna_1_3.write_question_CSV(question_name)
# ccna_1_3.write_choice_CSV(wrong_name)
# ccna_1_3.write_choice_CSV(right_name)

#
ccna_1_3.insert_question_DB('CCNA2v7.0_Modules 5 – 6_question.csv')
ccna_1_3.insert_choice_DB('CCNA2v7.0_Modules 5 – 6_wrong.csv')
ccna_1_3.insert_choice_DB('CCNA2v7.0_Modules 5 – 6_right.csv')