import xlrd, xlwt
from GPSPhoto import gpsphoto


if __name__ == "__main__":

    pachCSV = r'H:\фото ташт\1.xls'

    rb = xlrd.open_workbook(pachCSV, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    val = sheet.row_values(0)[0]
    vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
    photo = gpsphoto.GPSPhoto()
    pach_photo = r'H:\фото ташт\ташт фото'
    pach_itog = r'H:\фото ташт\itog'

    for i in vals:
        name = i[0]
        latitude = i[1]  #Широта
        longitude = i[2] #Долгота
        height = i[3] #высота

        pach_photo1 = pach_photo + "\\" + name + '.JPG'
        pach_itog1 = pach_itog + "\\" + name + '.JPG'
        print(pach_photo)
        print(pach_itog)
        try:
            photo = gpsphoto.GPSPhoto(pach_photo1)
            info = gpsphoto.GPSInfo((float(latitude), float(longitude)), alt=int(height * 10000))
            photo.modGPSData(info, pach_itog1)
        except FileNotFoundError:
            print("error")



