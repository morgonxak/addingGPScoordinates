from GPSPhoto import gpsphoto

# Create a GPSPhoto Object
photo = gpsphoto.GPSPhoto()
photo = gpsphoto.GPSPhoto(r"C:\Users\admin\EXIFparsing\pexif\test\data\noexif.jpg")

# Create GPSInfo Data Object

info = gpsphoto.GPSInfo((35.104860, -106.628915), alt=10)

# Modify GPS Data
photo.modGPSData(info, r"C:\Users\admin\EXIFparsing\pexif\test\data\noexif.jpg")

