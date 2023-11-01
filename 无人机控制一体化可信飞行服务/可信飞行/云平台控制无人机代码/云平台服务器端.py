def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(10)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("server start，wait for client connecting...")


def accept_client():
    """
    接收新连接
    """
    while True:
        client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client, info))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


def message_handle(client, info):
    """
    消息处理
    """
    global ground_lat, ground_lon, ground_alt

    client.sendall("connect server successfully!".encode(encoding='utf8'))
    while True:
        try:
            bytes = client.recv(2048)
            rec_time = time.time()
            msg = json.loads(bytes.decode(encoding='utf8'))
            cmd = msg[CMD]
            client_name = msg['client_name']

            if cmd == CONNECT:
                g_conn_pool[client_name] = client
                print('on client connect: ' + client_name, info)
            elif cmd == SEND_DATA:
                print(client_name + ': ' + msg[UAV_INFO])
            elif cmd == SET_G_LOCATION:
                ground_lat, ground_lon, ground_alt = msg[LAT], msg[LON], msg[ALT]
                print('地面站设置了lat：%lf, lon:%lf, alt: %lf' % (ground_lat, ground_lon, ground_alt))
            elif cmd == CAL_DIST_2UAV:
                cal_dist_uavs(msg[LAT], msg[LON], msg[ALT], client_name)
            elif cmd == CAL_DIST_G_U:
                l_dist = geodesic((msg[LAT], msg[LON]), (ground_lat, ground_lon)).meters
                h_dist = msg[ALT] - ground_alt
                dist = math.sqrt(l_dist * l_dist + h_dist * h_dist)
                print('distance between %s to ground: %lf m' % (client_name, dist))
            elif cmd == TIME_TEST:
                delay_time = (rec_time - msg[TIME]) * 1000 / 2
                i = msg['index'] + 1
                delay_list.append([i, delay_time])
                if i == msg['total']:
                    with open(msg['file'] + '.csv', 'a', encoding='utf-8', newline='') as file_obj:
                        writer = csv.writer(file_obj)
                        writer.writerows(delay_list)
                    delay_list = []
                    print('finish write %s' % msg['file'])

        except Exception as e:
            print(e)
            remove_client(client_name)
            break


def cal_dist_uavs(uav1_lat, uav1_lon, uav1_alt, client_name):
    global uav_location
    global COUNT_UAVs
    print('%s: lat : %lf ,lon: %lf, alt:%lf' % (client_name, uav1_lat, uav1_lon, uav1_alt))
    uav_location.append(uav1_lat)
    uav_location.append(uav1_lon)
    uav_location.append(uav1_alt)
    COUNT_UAVs += 1

    if COUNT_UAVs == 2:
        COUNT_UAVs = 0
        l_dist = geodesic((uav_location[0], uav_location[1]), (uav_location[3], uav_location[4])).meters
        h_dist = uav_location[2] - uav_location[5]
        dist_two_uav = math.sqrt(l_dist * l_dist + h_dist * h_dist)
        print('之间的距离为：%lf m' % dist_two_uav)
        uav_location = []


def remove_client(client_name):
    client = g_conn_pool[client_name]
    if client is not None:
        client.close()
        g_conn_pool.pop(client_name)
        print("client offline: " + client_name)


def send_data(op,data):
    if op == 'all':
        all_uavs_fly(data)
    elif op == 'multi':
        multi_uav_fly(data)
    else:
        print("ERROR INPUT!")


def multi_uav_fly(data):
    message = {}
    while True:
        uav_name = input('input client_name(-1 end input)：')
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        data = data
        msg = {CMD: UAV_FLY, 'data': data}
        message[uav] = msg
    for uav, msg in message.items():
        msg['time'] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))

def all_uavs_fly(data):
    data = data
    msg = {CMD: UAV_FLY, 'data': data}
    for uav in g_conn_pool.values():
        msg['time'] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        json_data = json.loads(post_data)
        option = json_data.get('option')
        data = json_data.get('data')

        print(f'Received option: {option}')
        print(f'Received data: {data}')
        send_data(option,data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Success')


def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    run(HTTPServer, RequestHandler, 6666)
    

