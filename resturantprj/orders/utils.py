import datetime

def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(pk)
    return current_time