import requests,json,csv,mysql.connector,pymongo
fp1=open("carts.json","w")
fp2=open('carts.csv','w',newline="")
cart_resp=requests.get('https://dummyjson.com/carts')
carts_data=cart_resp.json()

cart_csv_data=[]
cart_json_data=[]



for cart in carts_data["carts"]:
    #print(cart["id"])
    cart_json_data.append({"id":cart["id"],
                           "products":cart["products"],
                           "total":cart["total"],
                           "discountedTotal":cart["discountedTotal"],
                           "totalProducts":cart["totalProducts"],
                           "totalQuantity":cart["totalQuantity"]})
json.dump(cart_json_data,fp1)
print("New Json File Created")

fp1.close()



for cart in carts_data["carts"]:
    cart_csv_data.append((cart["id"],
                          json.dumps(cart["products"]),
                          cart["total"],
                          cart["discountedTotal"],
                          cart["totalProducts"],
                          cart["totalQuantity"]))
css_obj=csv.writer(fp2)
css_obj.writerow(["id","products","total","discountedTotal","totalProducts","totalQuantity"])
css_obj.writerows(cart_csv_data)
print("New CSS File Created")
    
    
fp2.close()



from pymongo import MongoClient
client=None
try:
    client=MongoClient('mongodb://localhost:27017/')
    db=client['Db1']
    user_col=db['Carts']
    user_col.insert_many(cart_json_data)
    print("user_col")
except:
    print("Error")
    
    
    
dbcon=None
cursor=None
try:
    dbcon=mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="root",
                                  database="dbcarts"
                                  ) 
    
    cursor=dbcon.cursor()
    sql_st='''
            CREATE TABLE if not exists carts (
            id INT,
            products JSON,
            total FLOAT,
            discountedTotal FLOAT,
            totalProducts FLOAT,
            totalQuantity FLOAT);
            '''
    sql_st1='''
            insert into carts(id,products,total,discountedTotal,totalProducts,totalQuantity) values(%s,%s,%s,%s,%s,%s);
            '''
            
        
    cursor.executemany(sql_st1,cart_csv_data) 
    dbcon.commit()
    print('New Mysql Table created Successfuly')
except mysql.connector.Error as err:
    print(err)

    
    