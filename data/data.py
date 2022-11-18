import os
import mysql.connector
import json

mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'), 
  user=os.getenv('MYSQL_USER'), 
  passwd=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE'),
)


# Opening JSON file
cursor = mydb.cursor()
url = 'taipei-attractions.json'
with open(url, mode='r', encoding='utf-8') as response:
    data = json.load(response)

# Iterating through the json
# list
data=data["result"]["results"]
for i in data:

    # insert into attraction table
    direction = i["direction"]
    name = i["name"]
    latitude = i['latitude']
    longitude = i["longitude"]
    MRT = i["MRT"]
    CAT = i["CAT"]
    description = i["description"]
    address = i["address"]
        
    file = i["file"]
    split_result = file.split("https:")
    image_list = []
    for x in split_result:
        if ".jpg" in x.lower() or ".png" in x.lower():
            image_url = "https:" + x
            image_list.append(image_url)
    
    # Insert attraction SQL
    sql = "INSERT INTO attraction(name, category, description, address, transport, mrt, latitude, longitude, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (name, CAT, description, address, direction, MRT, latitude, longitude, json.dumps(image_list))
    cursor.execute(sql, params)
    mydb.commit()
    
    # print(i['name'])
  