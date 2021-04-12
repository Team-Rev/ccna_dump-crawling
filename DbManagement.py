import pymysql
import csv
import pandas as pd
class Question:
    def __init__(self, exam, wrong_answer, answer):
        self.exam = exam
        self.wrong_answer = wrong_answer
        self.answer = answer
        self.conn = pymysql.connect(host='teamrev-db.cskul8vj3asp.ap-northeast-2.rds.amazonaws.com', user='root',
                               password='teamrev2021', db='question', charset='utf8', local_infile=1)
        self.cur = self.conn.cursor()

    def writeCSV(self, name):
        f = open(name, 'w', newline='')
        wr = csv.writer(f, delimiter='|')
        for i in range(len(self.exam)):
            try:
                wr.writerow(
                    str(self.exam[i])
                    , str(self.wrong_answer[i])
                    , str(self.answer[i])
                )
            except:
                wr.writerow(i+1, str(self.exam[i]), 'null', 'null')
        f.close()

    # def writeCSVtoPandas(self, name):
    #     df = pd.DataFrame(), columns=['exam', 'wrong_answer', 'answer']



    def insertDB(self, name):
        query = f"load data local infile 'C:\\\\Users\\\\User\\\\PycharmProjects\\\\pythonProject2\\\\selenium\\\\{name}' into table ccna_question fields terminated by '|' (exam,wrong_answer,answer);"
        self.cur.execute(query)
        self.conn.commit()
