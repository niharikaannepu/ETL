import requests,json,csv,mysql.connector,pymongo
fp1=open("carts.json","w")
fp2=open('carts.csv','w',newline="")
cart_resp=requests.get('https://dummyjson.com/carts')
carts_data=cart_resp.json()

cart_csv_data=[]
cart_json_data=[]

# print(users["carts"][0]["id"])
# print(users["carts"][0]["products"])
# # print(len(users["carts"][0]["products"]))


# print(users["carts"][0]["total"])
# print(users["carts"][0]["discountedTotal"])
# print(users["carts"][0]["userId"])
# print(users["carts"][0]["totalProducts"])
# print(users["carts"][0]["totalQuantity"])

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
                          cart["products"],
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