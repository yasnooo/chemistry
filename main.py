import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QStackedWidget, QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/z_window.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.reg)
        self.pushButton.clicked.connect(self.exit)
        self.line_edits = [self.lineEdit, self.lineEdit_2]

    def reg(self):
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        f = False
        res1 = cur.execute("""SELECT login FROM users""").fetchall()
        for i in range(len(res1)):
            if self.lineEdit.text() == res1[i][0]:
                QMessageBox.about(self, "Предупреждение", "Вы уже зарегистрированы или такой логин занят")
                f = True
                break
        if not f:
            flag = False
            num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for i in num:
                if i in self.lineEdit_2.text():
                    flag = True
            if len(self.lineEdit_2.text()) < 6 or not flag:
                QMessageBox.about(self, "Предупреждение",
                                  "Пароль должен содержать больше 5 символов и хотя бы одну цифру")
            else:
                user = (self.lineEdit.text(), self.lineEdit_2.text(), 0, 0, 0, 1, 0)
                cur.execute("""INSERT INTO users(login, password, progress, true, coins, lives, prop) 
                VALUES(?, ?, ?, ?, ?, ?, ?)""", user).fetchall()
                con.commit()
                con.close()
                global progress
                global true_ans
                global coins
                global lives
                lives = 1
                global prop
                prop = 0
                coins = 0
                progress = 0
                true_ans = 0
                window2 = Window2()
                widget.addWidget(window2)
                widget.setCurrentIndex(1)

    def exit(self):
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        k = 0
        res1 = cur.execute("""SELECT login FROM users""").fetchall()
        global log
        log = self.lineEdit.text()
        for i in range(len(res1)):
            if log != res1[i][0]:
                k += 1
        if k != len(res1):
            pas = cur.execute("""SELECT password FROM users where login = ?""", (log,)).fetchall()
            if self.lineEdit_2.text() != pas[0][0]:
                QMessageBox.about(self, "Предупреждение", "Неверный пароль")
            else:
                p = cur.execute("""SELECT progress FROM users where login = ?""", (log,)).fetchall()
                t = cur.execute("""SELECT true FROM users where login = ?""", (log,)).fetchall()
                c = cur.execute("""SELECT coins FROM users where login = ?""", (log,)).fetchall()
                pr = cur.execute("""SELECT prop FROM users where login = ?""", (log,)).fetchall()
                liv = cur.execute("""SELECT lives FROM users where login = ?""", (log,)).fetchall()
                global progress
                progress = p[0][0]
                global true_ans
                true_ans = t[0][0]
                global coins
                coins = c[0][0]
                global lives
                lives = liv[0][0]
                global prop
                prop = pr[0][0]
                window2 = Window2()
                widget.addWidget(window2)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            QMessageBox.about(self, "Предупреждение", "Вы еще не зарегистрированы")
        con.close()


class Window7(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/s_window.ui', self)
        self.initUI()

    def initUI(self):
        global a_games
        a_games = 0
        global f
        global lives
        global g_coins
        g_coins = 0
        self.g_lives = lives
        self.label_4.setText(self.label_4.text() + str(self.g_lives))
        self.pushButton.setText('Далее')
        self.pushButton_2.setText('пропуск хода:' + str(prop))
        global file_name
        if file_name:
            with open(file_name, encoding="utf8") as f:
                data = f.read()
            data = data.split('\n')
            self.quest = []
            self.forml = {}
            for i in data:
                i = i.split(',')
                self.forml[i[0]] = i[1][1:]
                self.forml[i[1][1:]] = i[0]
                self.quest.append(i[0])
                self.quest.append(i[1][1:])
        else:
            self.forml = {'HF': 'Плавиковая кислота', 'HCl': 'Соляная кислота', 'HBr': 'Бромоводородная кислота',
                          'H2S': 'Сероводородная кислота', 'HI': 'Иодоводородная кислота', 'H2SO4': 'Серная кислота',
                          'H2SO3': 'Сернистая кислота', 'HNO2': 'Азотистая кислота', 'HNO3': 'Азотная кислота',
                          'H3PO4': 'Ортофосфорная кислота', 'H2CO3': 'Угольная кислота', 'H2SiO3': 'Кремниевая кислота',
                          'AlCl3': 'Хлорид аллюминия', 'NaOH': 'Гидроксид натрия', 'Cl': 'Хлор', 'Ag': 'Серебро',
                          'Na': 'Натрий', 'S': 'Сера', 'Fe': 'Железо', 'Pb': 'Свинец', 'K': 'Калий',
                          'Zn(OH)2': 'Гидроксид цинка', 'Na2O': 'Оксид натрия', 'ZnO': 'Оксид цинка',
                          'CuSO4': 'Сульфат меди', 'Mg(NO3)2': 'Нитрат магния', 'ZnS': 'Сульфид цинка'}
            self.quest = ['HF', 'HCl', 'HBr', 'H2S', 'HI', 'H2SO4', 'H2SO3', 'HNO2', 'HNO3', 'H3PO4', 'H2CO3', 'H2SiO3',
                          'AlCl3', 'NaOH', 'Cl', 'Ag', 'Na', 'S', 'Fe', 'Pb', 'K', 'Zn(OH)2', 'Na2O', 'ZnO', 'CuSO4',
                          'Mg(NO3)2', 'ZnS']
        self.label_2.setText(random.choice(self.quest))
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.skip)

    def skip(self):
        global prop
        if prop == 0:
            QMessageBox.about(self, "Предупреждение", "Недостаточно пропусков")
        else:
            try:
                prop -= 1
                self.label_2.setText(random.choice(self.quest))
                self.lineEdit.setText('')
                self.label_3.setText('')
                self.pushButton_2.setText('пропуск хода:' + str(prop))
                global a_games
                global log
                con = sqlite3.connect('users.db')
                cur = con.cursor()
                result1 = cur.execute("""UPDATE users
                                            SET prop = ?
                                            WHERE login = ?""", (prop, log)).fetchall()
                con.commit()
                con.close()
            except Exception as e:
                print(e)

    def check(self):
        global coins
        global g_coins
        global a_games
        a_games += 1
        if self.label_2.text() == 'HF':
            if self.lineEdit.text() == self.forml[
                self.label_2.text()] or self.lineEdit.text() == 'Фтороводородная кислота':
                self.label_2.setText(random.choice(self.quest))
                self.lineEdit.setText('')
                self.label_3.setText('')
                coins += 1
                g_coins += 1
            else:
                self.label_3.setText('Неверно')
                self.g_lives -= 1
                if self.g_lives == 0:
                    window4 = Window4()
                    widget.addWidget(window4)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    self.label_4.setText('Жизни:' + str(self.g_lives))

        elif self.label_2.text() == 'HCl':
            if self.lineEdit.text() == self.forml[
                self.label_2.text()] or self.lineEdit.text() == 'Хлороводородная кислота':
                self.label_2.setText(random.choice(self.quest))
                self.lineEdit.setText('')
                self.label_3.setText('')

                coins += 1

                g_coins += 1
            else:
                self.label_3.setText('Неверно')
                self.g_lives -= 1
                if self.g_lives == 0:
                    window4 = Window4()
                    widget.addWidget(window4)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    self.label_4.setText('Жизни:' + str(self.g_lives))


        elif self.lineEdit.text() != self.forml[self.label_2.text()]:
            self.label_3.setText('Неверно')
            self.g_lives -= 1
            if self.g_lives == 0:
                window4 = Window4()
                widget.addWidget(window4)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.label_4.setText('Жизни:' + str(self.g_lives))
        else:
            self.label_2.setText(random.choice(self.quest))
            self.lineEdit.setText('')
            self.label_3.setText('')

            coins += 1

            g_coins += 1


class Window01(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/p_window.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.menu)

    def start(self):
        window7 = Window7()
        widget.addWidget(window7)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def menu(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window5(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/sixth_window.ui', self)
        self.initUI()

    def initUI(self):
        global coins
        self.live = 60
        self.skip = 40
        self.label_4.setText(str(coins))
        self.pushButton.clicked.connect(self.menu)
        self.pushButton_2.clicked.connect(self.buy_l)
        self.pushButton_3.clicked.connect(self.buy_s)

    def buy_l(self):
        global coins
        if int(coins) < self.live:
            QMessageBox.about(self, "Предупреждение", "Недостаточно монет")
        else:
            coins -= self.live
            self.label_4.setText(str(coins))
            global lives
            lives += 1
            global log
            try:
                con = sqlite3.connect('users.db')
                cur = con.cursor()
                result = cur.execute("""UPDATE users
                SET coins = ?
                WHERE login = ?""", (coins, log)).fetchall()
                con.commit()
                result1 = cur.execute("""UPDATE users
                                SET lives = ?
                                WHERE login = ?""", (lives, log)).fetchall()
                con.commit()
                con.close()
            except Exception as e:
                print(e)

    def buy_s(self):
        global coins
        global prop
        if coins < self.skip:
            QMessageBox.about(self, "Предупреждение", "Недостаточно монет")
        else:
            coins -= self.skip
            self.label_4.setText(str(coins))
            global prop
            prop += 1
            global log
            con = sqlite3.connect('users.db')
            cur = con.cursor()
            result = cur.execute("""UPDATE users
                            SET coins = ?
                            WHERE login = ?""", (coins, log)).fetchall()
            con.commit()
            result1 = cur.execute("""UPDATE users
                                            SET prop = ?
                                            WHERE login = ?""", (prop, log)).fetchall()
            con.commit()
            con.close()

    def menu(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window6(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/fi_window.ui', self)
        self.initUI()

    def initUI(self):
        global progress
        global true_ans
        self.label_4.setText(self.label_4.text() + ' ' + str(progress))
        self.label_5.setText(self.label_5.text() + ' ' + str(true_ans))
        self.pushButton.clicked.connect(self.menu)

    def menu(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window4(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/fo_window.ui', self)
        self.initUI()

    def initUI(self):
        global a_games
        global g_coins
        self.label_3.setText(str(g_coins) + '/' + str(a_games))
        self.label_5.setText('+' + str(g_coins))
        global progress
        progress += a_games
        global true_ans
        global log
        true_ans += g_coins
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        result = cur.execute("""UPDATE users
                                    SET progress = ?
                                    WHERE login = ?""", (progress, log)).fetchall()
        con.commit()
        result1 = cur.execute("""UPDATE users
                                        SET  true = ?
                                        WHERE login = ?""", (true_ans, log)).fetchall()
        con.commit()
        result2 = cur.execute("""UPDATE users
                                    SET coins = ?
                                    WHERE login = ?""", (coins, log)).fetchall()
        con.commit()
        con.close()
        self.pushButton.clicked.connect(self.back)

    def back(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window0(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/p_window.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.menu)

    def start(self):
        window3 = Window3()
        widget.addWidget(window3)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def menu(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window02(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/p_window.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.menu)

    def start(self):
        global file_name
        window7 = Window7()
        widget.addWidget(window7)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def menu(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/s_window.ui', self)
        self.initUI()

    def initUI(self):
        global a_games
        a_games = 0
        global f
        global lives
        global g_coins
        g_coins = 0
        self.g_lives = lives
        self.label_4.setText(self.label_4.text() + str(self.g_lives))
        self.forml = {'Плавиковая кислота': 'HF', 'Соляная кислота': 'HCl', 'Бромоводородная кислота': 'HBr',
                      'Сероводородная кислота': 'H2S', 'Иодоводородная кислота': 'HI', 'Серная кислота': 'H2SO4',
                      'Сернистая кислота': 'H2SO3', 'Азотистая кислота': 'HNO2', 'Азотная кислота': 'HNO3',
                      'Ортофосфорная кислота': 'H3PO4', 'Угольная кислота': 'H2CO3', 'Кремниевая кислота': 'H2SiO3',
                      'Хлорид аллюминия': 'AlCl3', 'Гидроксид натрия': 'NaOH', 'Хлор': 'Cl', 'Серебро': 'Ag',
                      'Натрий': 'Na', 'Сера': 'S', 'Железо': 'Fe', 'Свинец': 'Pb', 'Калий': 'K',
                      'Гидроксид цинка': 'Zn(OH)2', 'Оксид натрия': 'Na2O', 'Оксид цинка': 'ZnO',
                      'Сульфат меди': 'CuSO4', 'Нитрат магния': 'Mg(NO3)2', 'Хлорид железа(II)': 'FeCl2',
                      'Сульфид цинка': 'ZnS'}
        self.quest = ['Плавиковая кислота', 'Соляная кислота', 'Бромоводородная кислота', 'Сероводородная кислота',
                      'Иодоводородная кислота', 'Серная кислота', 'Сернистая кислота', 'Азотистая кислота',
                      'Азотная кислота', 'Ортофосфорная кислота', 'Угольная кислота', 'Кремниевая кислота',
                      'Хлорид аллюминия', 'Гидроксид натрия', 'Хлор', 'Серебро', 'Натрий', 'Сера', 'Железо', 'Свинец',
                      'Калий', 'Гидроксид цинка', 'Оксид натрия', 'Оксид цинка', 'Сульфат меди', 'Нитрат магния',
                      'Хлорид железа(II)', 'Сульфид цинка']
        self.pushButton.setText('Далее')
        self.pushButton_2.setText('пропуск хода:' + str(prop))
        self.label_2.setText(random.choice(self.quest))
        self.pushButton.clicked.connect(self.check)
        self.pushButton_2.clicked.connect(self.skip)

    def skip(self):
        global prop
        if prop == 0:
            QMessageBox.about(self, "Предупреждение", "Недостаточно пропусков")
        else:
            try:
                prop -= 1
                self.label_2.setText(random.choice(self.quest))
                self.lineEdit.setText('')
                self.label_3.setText('')
                self.pushButton_2.setText('пропуск хода:' + str(prop))
                global a_games
                global log
                con = sqlite3.connect('users.db')
                cur = con.cursor()
                result1 = cur.execute("""UPDATE users
                                    SET prop = ?
                                    WHERE login = ?""", (prop, log)).fetchall()
                con.commit()
                con.close()
            except Exception as e:
                print(e)

    def check(self):
        try:
            global a_games
            a_games += 1
            if self.lineEdit.text() != self.forml[self.label_2.text()]:
                self.label_3.setText('Неверно')
                self.g_lives -= 1
                if self.g_lives == 0:
                    window4 = Window4()
                    widget.addWidget(window4)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:
                    self.label_4.setText('Жизни:' + str(self.g_lives))
            else:
                self.label_2.setText(random.choice(self.quest))
                self.lineEdit.setText('')
                self.label_3.setText('')
                global coins
                coins += 1
                global g_coins
                g_coins += 1
        except Exception as e:
            print(e)


class Window_d(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/download.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton_3.clicked.connect(self.download_f)
        self.pushButton.clicked.connect(self.go_to)
        self.pushButton_2.clicked.connect(self.go_back)

    def download_f(self):
        global file_name
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Текстовый документ (*.txt);;Все файлы (*)')[0]
        file_name = fname

    def go_to(self):
        global file_name
        if file_name:
            window02 = Window02()
            widget.addWidget(window02)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.label_5.setText('Вы не выбрали файл')

    def go_back(self):
        window2 = Window2()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uic/f_window.ui', self)
        self.initUI()

    def initUI(self):
        global coins
        self.label_4.setText(str(coins))
        self.pushButton_3.clicked.connect(self.shop)
        self.pushButton_5.clicked.connect(self.stat)
        self.pushButton.clicked.connect(self.w_formul)
        self.pushButton_2.clicked.connect(self.w_text)
        self.pushButton_6.clicked.connect(self.download)

    def download(self):
        try:
            window_d = Window_d()
            widget.addWidget(window_d)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def w_text(self):
        window01 = Window01()
        widget.addWidget(window01)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def w_formul(self):
        try:
            window0 = Window0()
            widget.addWidget(window0)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            print(e)

    def shop(self):
        window5 = Window5()
        widget.addWidget(window5)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def stat(self):
        window6 = Window6()
        widget.addWidget(window6)
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    f = True
    log = ''
    # переменные, которые по умолчанию используются для добавления данных про новых пользователей
    a_games = 0
    progress = 0
    true_ans = 0
    coins = 0
    lives = 1
    prop = 0
    # переменная, считающая количестов монет за одну игру
    g_coins = 0
    file_name = ''
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    main = MyWidget()
    widget.addWidget(main)
    widget.setWindowTitle('Химический тренажер')
    widget.setFixedHeight(640)
    widget.setFixedWidth(687)
    widget.show()
    sys.exit(app.exec_())
