import xlrd, xlwt
from GPSPhoto import gpsphoto
import threading
import os



def getHeight(number):
    s = str(number)

    temp1 = abs(s.find('.') - len(s)) - 1
    n = int('1' + '0' * temp1)

    #print(type(number),n,temp1)
    numberT = number * n
    return (int(numberT), n)

def fileSplitting(flow, vals):
    '''
    Возвращает масив с начальной точкой и конечной точкой для каждого потока
    :param flow:  #Количество потоков
    :param vals:  #масив с данными
    :return:
    '''
    quantityImage = len(vals)  # всего изображений
    streams = []  # Потоки
    dStream = quantityImage // flow

    startingLine = 0
    endLine = dStream
    for i in range(flow - 1):
        streams.append((startingLine, endLine))
        startingLine = startingLine + dStream + 1
        endLine = endLine + dStream + 1

    startingLine = startingLine
    endLine = (quantityImage - endLine) + endLine
    streams.append((startingLine, endLine))
    return streams

def startStreams(startImange,endImage,vals,pach_photo,pach_itog):
    '''
    Функция формирования потока принимает список с именами, начальная и конечная строка откуда брать изображения и куда его отдовать
    :param startImange:
    :param endImage:
    :param vals:
    :param pach_photo:
    :param pach_itog:
    :return:
    '''
    lenVals = len(vals)
    print("Всего фоографий", lenVals)
    deltaProgressBar = 100 / lenVals

    for i in range(startImange, endImage+1):
        try:

            name = vals[i][0]
            latitude = vals[i][1]  #Широта
            longitude = vals[i][2] #Долгота
            height = vals[i][3] #высота

            #pach_photo1 = pach_photo + "\\" + name
            pach_photo1 = os.path.join(pach_photo, name)
            #pach_itog1 = pach_itog + "\\" + name
            pach_itog1 = os.path.join(pach_itog, name)

            #print(i, name,latitude,longitude,height)

            tempH = getHeight(float(height))
            photo = gpsphoto.GPSPhoto(pach_photo1)
            info = gpsphoto.GPSInfo((float(latitude), float(longitude)), alt=tempH[0], altDel=tempH[1])
            photo.modGPSData(info, pach_itog1)

            #print("Количество обработанных фотографий в потоке", startImange, "-", endImage, "обработанно", t)
        except BaseException as e:
            print("Ошибка")
            print("Поток", startImange, "-", endImage, "имя", name)
            print(e)

        if progressBar != None:
            print("progressBar", progressBar.value(), deltaProgressBar, progressBar.value() + deltaProgressBar)
            temp = progressBar.value() + deltaProgressBar
            progressBar.setValue(temp)
    print("Поток завершон", startImange, "-", endImage)


if __name__ == "__main__":

    pachCSV = r'E:\geo.xls'
    pach_photo = r'E:\3'

    pach_itog = pach_photo

    rb = xlrd.open_workbook(pachCSV, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    val = sheet.row_values(0)[0]
    vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
    streams = fileSplitting(10, vals)

    ths = []
    for stream in streams:
        ths.append(threading.Thread(target=startStreams, args=(stream[0], stream[1], vals, pach_photo, pach_itog)))
        print("инициализация потока", stream)

    for i in ths:
        i.start()
