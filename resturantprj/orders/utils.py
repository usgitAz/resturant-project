import datetime
import json
def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(pk)
    return current_time


def order_total_by_vendor (order , vendor_id ):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(vendor_id))
    sunbtotal = 0
    tax = 0
    tax_dict = {}

    for key , value in data.items() :
        sunbtotal += float(key)
        value = value.replace("'" , '"')
        value = json.loads(value)
        tax_dict.update(value)

        #calc tax
        #EVAT': {'9.00': '8.64'}}
        for i in value :
            for j in value[i] :
                tax = float(value[i][j]) #ex: 4.32 

    total =  float(sunbtotal) + float(tax)                      
    context = {
        'subtotal' : sunbtotal ,
        'total' : total , 
        'tax_dict' : tax_dict 
    }
    return context