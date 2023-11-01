def send_request(option, data):
    url = 'http://localhost:6666'
    payload = {
        'option': option,
        'data': data
    }
    headers = {
        'Content-type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print('Request sent successfully')
    else:
        print('Error sending request')

def isInt(num):
    try:
        num = int(str(num))
        return isinstance(num, int)
    except:
        return False
    
def check(tmp):
    for i in tmp:
        if isInt(i)==False:
            return False
    return True

def data_input():
    while True:
        strvar = input("input instruction(x:,y:,z:,duration: ):")
        plain = strvar
        strvar = strvar.split(' ')
        if (len(strvar) == 1 and plain.upper() != 'Q' and plain.upper() != 'L' and plain.upper() != 'F') or (
                len(strvar) != 1 and len(strvar) != 4) or (len(strvar)==4 and check(strvar)==False):
            print("wrong input!")
            continue
        break
    return plain

def op_input():
    while True:
        op = input('Enter option: ')
        if (op == "all") or (op =="multi") or (op == TIME_TEST) or (op == SEND_GROUND_LOCATION) or (op in (SET_G_LOCATION, CAL_DIST_G_U)) or (op == SET_G_L) or (op == CAL_DIST_2UAV) or (op in (QUERY_BATTERY, CHANGE_PARAM_GOOD, CHANGE_PARAM_BAD)):
            break
        print("wrong option input!")
    return op

if __name__ == '__main__':
    while True:
        option = op_input()
        data = data_input()
        send_request(option, data)