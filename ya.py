import os
import sys
import sqlite3
from urllib.parse import urlparse

#get the path to browser's data
path = "C:\\Users\\{}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data".format(os.getlogin())
while not os.path.exists(path):
    print("{} doesn't exist!".format(path))
    path = input("Enter path to yandex browser's user data directory:")


#if there are profiles, then user should choose which one to use
#otherwise default will be used

is_profile_dir = lambda a: "Profile" in a
profiles = filter(is_profile_dir,os.listdir())
should_choose_profile = lambda: len(list(profiles)) != 0

target = "Default"
if not should_choose_profile:
    print(":Existing profiles:")
    for id,p in enumerate(profiles): print("({}){}".format(id,p))

    inp = input("enter profile number:")
    if not inp.isdigit():
        print("incorrect profile number!")
        sys.exit()
    if int(inp) > len(profiles) or int(inp) < 0:
        print("incorrect profile number!")
        sys.exit()

    target = "Profile {}".format(int(inp))

#obtain path to database
path = path + "\\"+target+"\\"+"History"


#open database and fetch all data
con = sqlite3.connect(path)
cur = con.cursor()
data = cur.execute("SELECT * FROM urls")
result = data.fetchall()

#compute the statistic
urls = {}
for r in result:
    url = urlparse(r[1]).netloc
    if url not in urls.keys():
        urls[url] = 1
    else:
        urls[url] += 1

sorted_urls =  {k: v for k, v in sorted(urls.items(), key=lambda item: item[1], reverse=True)}

counter = 0
for url in sorted_urls:
    if counter == 10:
        input("press ENTER to continue...")
        counter = 0

    count = sorted_urls[url]
    align_value = abs(20-len(url))
    print("{}{}  ::: visiting frequency = {} ::: percentage = {} %".format(url," "*align_value,count, count/len(urls.keys())))
    counter+=1
    
