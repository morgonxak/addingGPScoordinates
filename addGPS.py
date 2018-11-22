from GPSPhoto import gpsphoto

# Create a GPSPhoto Object
photo = gpsphoto.GPSPhoto()
pachPhoto  = r"C:\Users\admin\PycharmProjects\untitled3\1.jpg"
photo = gpsphoto.GPSPhoto(pachPhoto)

# Create GPSInfo Data Object

info = gpsphoto.GPSInfo((35.104860, -106.628915), alt=3925203)  #3925203000 392.5203

# Modify GPS Data
photo.modGPSData(info, pachPhoto)

