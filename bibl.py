import sqlite3


class info_people:
    def __init__(self, id, name, age, city, about, png):
        self.id = id
        self.name = name
        self.age = age
        self.city = city
        self.about = about
        self.img = png

    def __str__(self):
        return self.name + ', возраст - ' + str(self.age) + ', город ' + self.city


sovm = {'ENTJ-ISFP': 99, 'ENTJ-INFP': 91, 'ENTJ-ESFP': 81, 'ENTJ-ESTP': 71, 'ENTJ-ISTP': 61,
        'ENTJ-INTP': 51, 'ENTJ-ENFP': 41, 'ENTJ-INFJ': 31, 'ENTJ-INTJ': 21, 'ENTJ-ENFJ': 19, 'ENTJ-ISTJ': 15,
        'ENTJ-ENTP': 10, 'ENTJ-ESTJ': 5, 'ENTJ-ENTJ': 4, 'ENTJ-ESFJ': 2, 'ENTJ-ISFJ': 1,

        'ENTP-ISFJ': 99, 'ENTP-ISTJ': 91, 'ENTP-ENTP': 81, 'ENTP-ESTJ': 71, 'ENTP-ESFJ': 61,
        'ENTP-INFJ': 51, 'ENTP-INTJ': 41, 'ENTP-INFP': 31, 'ENTP-ENFJ': 21, 'ENTP-INTP': 19, 'ENTP-ISTP': 15,
        'ENTP-ENFP': 10, 'ENTP-ESTP': 5, 'ENTP-ENTJ': 4, 'ENTP-ESFP': 2, 'ENTP-ISFP': 1,

        'INTJ-ESFP': 99, 'INTJ-ESTP': 91, 'INTJ-ISFP': 81, 'INTJ-INFP': 71, 'INTJ-INFJ': 61,
        'INTJ-ENFP': 51, 'INTJ-ENTP': 41, 'INTJ-ISTP': 31, 'INTJ-ENFJ': 21, 'INTJ-INTJ': 19, 'INTJ-ISTJ': 15,
        'INTJ-ENTJ': 10, 'INTJ-INTP': 5, 'INTJ-ESTJ': 4, 'INTJ-ISFJ': 2, 'INTJ-ESFJ': 1,

        'INTP-ESFJ': 99, 'INTP-ENFJ': 91, 'INTP-ISFJ': 81, 'INTP-INFJ': 71, 'INTP-ESTJ': 61,
        'INTP-ISTJ': 51, 'INTP-ENTJ': 41, 'INTP-ENFP': 31, 'INTP-ENTP': 21, 'INTP-INTP': 19, 'INTP-INTJ': 15,
        'INTP-ISTP': 10, 'INTP-INFP': 5, 'INTP-ESTP': 4, 'INTP-ISFP': 2, 'INTP-ESFP': 1,

        'ESTJ-INFP': 99, 'ESTJ-ISFP': 91, 'ESTJ-INTP': 81, 'ESTJ-ENTP': 71, 'ESTJ-ISTP': 61,
        'ESTJ-ESFP': 51, 'ESTJ-ENFP': 41, 'ESTJ-ISTJ': 31, 'ESTJ-ISFJ': 21, 'ESTJ-ESTJ': 19, 'ESTJ-ESFJ': 15,
        'ESTJ-INTJ': 10, 'ESTJ-ENTJ': 5, 'ESTJ-ESTP': 4, 'ESTJ-ENFJ': 2, 'ESTJ-INFJ': 1,

        'ESFJ-INTP': 99, 'ESFJ-ISTP': 91, 'ESFJ-ENTP': 81, 'ESFJ-ENFP': 71, 'ESFJ-INFP': 61,
        'ESFJ-ISTJ': 51, 'ESFJ-ESFJ': 41, 'ESFJ-ESTP': 31, 'ESFJ-ISFP': 21, 'ESFJ-ENFJ': 19, 'ESFJ-ISFJ': 15,
        'ESFJ-INFJ': 10, 'ESFJ-ESTJ': 5, 'ESFJ-ESFP': 4, 'ESFJ-ENTJ': 2, 'ESFJ-INTJ': 1,

        'ISTJ-ENFP': 99, 'ISTJ-ENTP': 91, 'ISTJ-ISFP': 81, 'ISTJ-INFP': 71, 'ISTJ-ESTP': 61,
        'ISTJ-ESFP': 51, 'ISTJ-INTP': 41, 'ISTJ-ESTJ': 31, 'ISTJ-ESFJ': 21, 'ISTJ-ISTJ': 19, 'ISTJ-INTJ': 15,
        'ISTJ-ISFJ': 10, 'ISTJ-ISTP': 5, 'ISTJ-ENTJ': 4, 'ISTJ-INFJ': 2, 'ISTJ-ENFJ': 1,

        'ISFJ-ENTP': 99, 'ISFJ-ENFP': 91, 'ISFJ-INTP': 81, 'ISFJ-ISTP': 71, 'ISFJ-ESFP': 61,
        'ISFJ-ESTP': 51, 'ISFJ-ESTJ': 41, 'ISFJ-INFP': 31, 'ISFJ-ESFJ': 21, 'ISFJ-ISTJ': 19, 'ISFJ-ISFJ': 15,
        'ISFJ-ENFJ': 10, 'ISFJ-INFJ': 5, 'ISFJ-ISFP': 4, 'ISFJ-INTJ': 2, 'ISFJ-ENTJ': 1,

        'ENFJ-ISTP': 99, 'ENFJ-INTP': 91, 'ENFJ-ESTP': 81, 'ENFJ-ESFP': 71, 'ENFJ-ENFJ': 61,
        'ENFJ-INFP': 51, 'ENFJ-ISFP': 41, 'ENFJ-ENTP': 31, 'ENFJ-INTJ': 21, 'ENFJ-ESFJ': 19, 'ENFJ-INFJ': 15,
        'ENFJ-ENFP': 10, 'ENFJ-ENTJ': 5, 'ENFJ-ISFJ': 4, 'ENFJ-ESTJ': 2, 'ENFJ-ISTJ': 1,

        'ENFP-ISTJ': 99, 'ENFP-ISFJ': 91, 'ENFP-ESFJ': 81, 'ENFP-ESTJ': 71, 'ENFP-INFJ': 61,
        'ENFP-INTJ': 51, 'ENFP-ENTJ': 41, 'ENFP-ISFP': 31, 'ENFP-ENFP': 21, 'ENFP-INTP': 19, 'ENFP-INFP': 15,
        'ENFP-ENFJ': 10, 'ENFP-ENTP': 5, 'ENFP-ESFP': 4, 'ENFP-ESTP': 2, 'ENFP-ISTP': 1,

        'INFJ-ESTP': 99, 'INFJ-ESFP': 91, 'INFJ-ISTP': 81, 'INFJ-INTP': 71, 'INFJ-ENFP': 61,
        'INFJ-ENTP': 51, 'INFJ-INTJ': 41, 'INFJ-ENTJ': 31, 'INFJ-INFJ': 21, 'INFJ-ISFP': 19, 'INFJ-ENFJ': 15,
        'INFJ-ESFJ': 10, 'INFJ-ISFJ': 5, 'INFJ-INFP': 4, 'INFJ-ISTJ': 2, 'INFJ-ESTJ': 1,

        'INFP-ESTJ': 99, 'INFP-ENTJ': 91, 'INFP-INTJ': 81, 'INFP-ISTJ': 71, 'INFP-ENFJ': 61,
        'INFP-ESFJ': 51, 'INFP-ENTP': 41, 'INFP-INFP': 31, 'INFP-ISFJ': 21, 'INFP-INTP': 19, 'INFP-ESFP': 15,
        'INFP-ENFP': 10, 'INFP-ISFP': 5, 'INFP-INFJ': 4, 'INFP-ISTP': 2, 'INFP-ESTP': 1,

        'ESTP-INFJ': 99, 'ESTP-INTJ': 91, 'ESTP-ENFJ': 81, 'ESTP-ENTJ': 71, 'ESTP-ISFJ': 61,
        'ESTP-ISTP': 51, 'ESTP-ISTJ': 41, 'ESTP-ESFJ': 31, 'ESTP-ESTP': 21, 'ESTP-ISFP': 19, 'ESTP-ESFP': 15,
        'ESTP-INTP': 10, 'ESTP-ENTP': 5, 'ESTP-ESTJ': 4, 'ESTP-ENFP': 2, 'ESTP-INFP': 1,

        'ESFP-INTJ': 99, 'ESFP-INFJ': 91, 'ESFP-ENTJ': 81, 'ESFP-ENFJ': 71, 'ESFP-ESTJ': 61,
        'ESFP-ISTJ': 51, 'ESFP-ISFJ': 41, 'ESFP-ISFP': 31, 'ESFP-ISTP': 21, 'ESFP-INFP': 19, 'ESFP-ESFP': 15,
        'ESFP-ESTP': 10, 'ESFP-ESFJ': 5, 'ESFP-ENFP': 4, 'ESFP-ENTP': 2, 'ESFP-INTP': 1,

        'ISTP-ENFJ': 99, 'ISTP-ESFJ': 91, 'ISTP-INFJ': 81, 'ISTP-ISFJ': 71, 'ISTP-ENTJ': 61,
        'ISTP-ESTJ': 51, 'ISTP-ESFP': 41, 'ISTP-ESTP': 31, 'ISTP-INTJ': 21, 'ISTP-ISTP': 19, 'ISTP-INTP': 15,
        'ISTP-ENTP': 10, 'ISTP-ISTJ': 5, 'ISTP-ISFP': 4, 'ISTP-INFP': 2, 'ISTP-ENFP': 1,

        'ISFP-ENTJ': 99, 'ISFP-ESTJ': 91, 'ISFP-INTJ': 81, 'ISFP-ISTJ': 71, 'ISFP-ENFJ': 61,
        'ISFP-ESFJ': 51, 'ISFP-INFJ': 41, 'ISFP-ESFP': 31, 'ISFP-ISFP': 21, 'ISFP-ESTP': 19, 'ISFP-ENFP': 15,
        'ISFP-INFP': 10, 'ISFP-ISTP': 5, 'ISFP-ISFJ': 4, 'ISFP-INTP': 2, 'ISFP-ENTP': 1
        }


def sovmest(id):
    # Подключение к БД
    con = sqlite3.connect("db/data.db")
    # Создание курсора
    cur = con.cursor()

    cur.execute("SELECT * FROM pr_test WHERE ID = " + str(id) + ";")
    res = cur.fetchall()
    print(res)
    id_r = ''.join(res[0][1:])
    print(id_r)
    cur.execute("SELECT * FROM pr_test;")
    results = cur.fetchall()
    sp_rez = []
    for st in results:
        if st[0] != id:
            s = ''.join(st[1:])
            s1 = id_r + '-' + s
            s2 = s + '-' + id_r
            print(s1, s2)
            if s1 in sovm:
                sp_rez.append([st[0], sovm[s1]])
            elif s2 in sovm:
                sp_rez.append([st[0], sovm[s2]])
    sp_rez.sort(key=lambda i: i[1], reverse=True)
    cur.execute("SELECT * FROM users;")
    res = cur.fetchall()
    sp_r = []
    for b in sp_rez:
        for st in res:
            if st[0] == b[0]:
                sp_r.append(info_people(st[0], st[1], st[2], st[3], st[4], st[5]))
    return sp_r
