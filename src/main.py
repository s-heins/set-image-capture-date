from datetime import datetime
import os
import re
import piexif
import time


# changed from https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            fullPath = os.path.abspath(os.path.join(dirpath, f))
            if re.match(r"^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}.*", f):
                print(f+" Matched")
                
                match = re.search("^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}).*", f)
                year = int(match.group(1))
                month= int(match.group(2))
                day = int(match.group(3))
                hour = int(match.group(4))
                minutes = int(match.group(5))
                seconds = int(match.group(6))

                updateExifData(fullPath, year, month, day, hour, minutes, seconds)
                setUpdatedTime(fullPath, year, month, day, hour, minutes, seconds)

                print("############################")

def updateExifData(fullPath, year, month, day, hour, minutes, seconds):
   exif_dict = piexif.load(fullPath)
   datetimeString = datetime(year,month,day,hour,minutes,seconds).strftime("%Y:%m:%d %H:%M:%S")
                
   print(datetimeString + " is datetimeString")
                
   #Update DateTimeOriginal
   print(str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]) + "is current DateTimeOriginal")
   exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = datetimeString

   #Update DateTimeDigitized               
   exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = datetimeString
   
   #Update DateTime
   exif_dict['0th'][piexif.ImageIFD.DateTime] = datetimeString
   
   exif_bytes = piexif.dump(exif_dict)
   piexif.insert(exif_bytes, fullPath) 

def setUpdatedTime(fullPath, year, month, day, hour, minutes, seconds):
    date = datetime(year=year, month=month, day=day, hour=hour, minute=minutes, second=seconds)
    modifiedTime = time.mktime(date.timetuple())

    print("Modified date: " + str(date))
    os.utime(fullPath, (modifiedTime, modifiedTime))

def run():
    absoluteFilePaths("__SET-DIRECTORY__")