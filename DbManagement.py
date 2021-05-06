import pymysql
import csv
import pandas as pd
import sys

import io

class Question:
    def __init__(self, exam, main_category, sub_category, wrong_answer, answer):
        self.exam = exam
        self.main_category = main_category
        self.sub_category = sub_category
        self.wrong_answer = wrong_answer
        self.answer = answer
        self.conn = pymysql.connect(host='******', user='root',
                               password='******', db='rev_problem', charset='utf8', local_infile=1)
        self.cur = self.conn.cursor()
        self.count = 0

    def write_question_CSV(self, name):
        self.cur.execute('select count(*) from question')
        index = self.cur.fetchone()
        index_value = index[0]

        f = open(name, 'w', newline='', encoding='utf-8')
        wr = csv.writer(f, delimiter='|')
        for i in range(len(self.exam)):
            wr.writerow([str(index_value+1), str(self.exam[i]),str(self.main_category),str(self.sub_category)])
            index_value += 1
        f.close()



    def write_choice_CSV(self, name):

        self.cur.execute('select count(*) from question')
        index_qu = self.cur.fetchone()
        index_value = index_qu[0]
        f = open(name, 'w', newline='', encoding='utf-8')
        wr = csv.writer(f, delimiter='|')
        if name[-9:-4] == 'wrong':
            for i in range(len(self.wrong_answer)):
                for j in range(len(self.wrong_answer[i])):
                    wr.writerow([str('0'),str(self.wrong_answer[i][j]),str(index_value+1)])
                index_value += 1
            f.close()
        elif name[-9:-4] == 'right':
            for i in range(len(self.answer)):
                for j in range(len(self.answer[i])):
                    wr.writerow([str('1'), str(self.answer[i][j]), str(index_value + 1)])
                index_value += 1
            f.close()


    def insert_question_DB(self, name):
        query = f"load data local infile 'C:\\\\Users\\\\User\\\\PycharmProjects\\\\pythonProject2\\\\selenium\\\\{name}' into table question fields terminated by '|' (id,exam,main_category,sub_category);"
        self.cur.execute(query)
        self.conn.commit()

    def insert_choice_DB(self, name):
        query = f"load data local infile 'C:\\\\Users\\\\User\\\\PycharmProjects\\\\pythonProject2\\\\selenium\\\\{name}' into table multiple_choice fields terminated by '|' (is_correct,choice,question_id);"
        self.cur.execute(query)
        self.conn.commit()


