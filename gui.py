import sys  # sys нужен для передачи argv в QApplication
import disain  # Это наш конвертированный файл дизайна

from PyQt5 import QtCore, QtGui, QtWidgets
import pullGPS
import xlrd, xlwt

import os
import threading

class imageGUIGPS(QtWidgets.QMainWindow, disain.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        self.pathXml = None
        self.pathImage = None
        self.pathImageItog = None
        self.stateThreading = None

        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # при нажатии кнопки
        #self.pushButton.clicked.connect(self.SetPachImage)
        self.pushButton.clicked.connect(self.openXml)
        self.pushButton_2.clicked.connect(self.openPathImage)
        self.pushButton_4.clicked.connect(self.exampleXML)
        self.pushButton_3.clicked.connect(self.openPathImageItog)
        self.pushButton_5.clicked.connect(self.start)

        self.progressBar.setValue(0)

    def startStreams(self, startImange, endImage, vals, pach_photo, pach_itog):
        '''
        Функция формирования потока принимает список с именами, начальная и конечная строка откуда брать изображения и куда его отдовать
        :param startImange:
        :param endImage:
        :param vals:
        :param pach_photo:
        :param pach_itog:
        :return:
        '''
        deltaProgressBar = 1  #Для бара

        for i in range(startImange, endImage + 1):
            try:
                if self.stateThreading:
                    name = vals[i][0]
                    latitude = vals[i][1]  # Широта
                    longitude = vals[i][2]  # Долгота
                    height = vals[i][3]  # высота

                    # pach_photo1 = pach_photo + "\\" + name
                    pach_photo1 = os.path.join(pach_photo, name)
                    # pach_itog1 = pach_itog + "\\" + name
                    pach_itog1 = os.path.join(pach_itog, name)

                    # print(i, name,latitude,longitude,height)

                    tempH = pullGPS.getHeight(float(height))
                    photo = pullGPS.gpsphoto.GPSPhoto(pach_photo1)
                    info = pullGPS.gpsphoto.GPSInfo((float(latitude), float(longitude)), alt=tempH[0], altDel=tempH[1])
                    photo.modGPSData(info, pach_itog1)

                    print("progressBar", self.progressBar.value(), deltaProgressBar,
                          self.progressBar.value() + deltaProgressBar)
                    temp = self.progressBar.value() + deltaProgressBar
                    self.progressBar.setValue(temp)
                else:
                    print("Экстренная остоновка потока")
                    break

            except BaseException as e:
                print("Ошибка")
                print("Поток", startImange, "-", endImage, "имя", name)
                print(e)

        print("Поток завершон", startImange, "-", endImage)


    def openXml(self):
        '''
        ОТкрыть диологовое окно формат xml
        :return: C:/Users/admin/PycharmProjects/untitled3/test.xls
        '''
        print("openXml")

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Файл с географическими координатами', '/home', filter='*.xls')[0]
        self.pathXml = fname
        return fname

    def openPathImage(self):
        '''
        открыть диологовое окно до папки
        :return: C:/Users/admin/PycharmProjects/untitled3/GUI
        '''
        print("openPathImage")

        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Укажите попку с исходными фотографиями')
        self.pathImage = fname
        listFnane = os.listdir(fname)
        self.label_6.setText(str(len(listFnane)) + ' штук')

        self.progressBar.setMaximum(len(listFnane))  #Задаем для ProgressBar максимальное число
        return fname

    def openPathImageItog(self):
        '''
        открыть диологовое окно до папки
        :return:
        '''
        print("openPathImageItog")
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Укажите попку с результирующими фотографиями')
        self.pathImageItog = fname
        return fname

    def exampleXML(self):
        '''
        открыть xml примера
        :return:
        '''
        print("exampleXML")
        QtWidgets.QMessageBox.question(self, "Файл лежит там же где проект ",
                                       QtWidgets.QMessageBox.Yes)

    def validationButton(self):
        '''
        Валидация кнопок
        :return:
        '''
        if self.pathXml == None or self.pathImage == None or self.pathImageItog == None:
            return True
        else:
            return False

    def start(self):
        print("Start")
        print(self.validationButton())
        if self.validationButton():
            QtWidgets.QMessageBox.question(self, 'Предупреждение',
                                           "Указанны не все параметры",
                                           QtWidgets.QMessageBox.Yes)
        else:
            if self.pushButton_5.text() == "Пуск":
                rb = xlrd.open_workbook(self.pathXml, formatting_info=True)
                sheet = rb.sheet_by_index(0)
                vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
                streams = pullGPS.fileSplitting(self.spinBox.value(), vals)

                ths = []

                for stream in streams:
                    ths.append(threading.Thread(target=self.startStreams, args=(stream[0], stream[1], vals, self.pathImage, self.pathImageItog)))
                    print("инициализация потока", stream)
                self.stateThreading = True
                for i in ths:
                    i.start()
                self.pushButton_5.setText("Стоп")
            else:
                self.pushButton_5.setText("Пуск")
                self.stateThreading = False
                self.progressBar.setValue(0)


def main():
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = imageGUIGPS()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()