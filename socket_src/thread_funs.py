# 젯슨나노 음성자모음 클라이언트
def communication_with_python(client_socket, addr):
    global python_to_unity_queue, count_connectied_jetson
    # 서버ip : 클라이언트 포트
    print('젯슨나노 접속성공!(', addr[0], ':', addr[1],')') 

    while True: 
        try:
            data = client_socket.recv(1024)
            if not data:
                #print('젯슨나노 연결 종료' + addr[0],':',addr[1])
                break
            print(data.decode().strip())
            #python_to_unity_queue.put(data)
            
        except ConnectionResetError as e:
            #print('Disconnected by 젯슨 예외처리')
            break

    print('젯슨나노 연결 종료' + addr[0],':',addr[1]) # 예외발생시 젯슨과의 tcp연결 종료를 알리는 디벙깅용함수
    client_socket.close() #젯슨 과의 클라이언트 연결 종료
    
    
# 유니티 클라이언트
def communication_with_unity(client_socket, addr): 
    global python_to_unity_queue
    # 서버ip : 클라이언트 포트
    print('유니티접속 성공!(', addr[0], ':', addr[1],')') 

    while True: 
        try:
            data_from_unity = client_socket.recv(1024)
            if not data_from_unity: 
                print('유니티 연결 종료 ' + addr[0],':',addr[1])
                break
            
            # if data_from_unity == 'ChangeHanddetectionMode':
            #     client_socket.sendall('ChangeHanddetectionMode'.encode())
            # elif data_from_unity == 'ChangListenMode':

            data_from_queue = python_to_unity_queue.get() #큐의 맨앞에서 encode()형의 데이터를 가져온다.
            if data_from_queue: #데이터 값이 존재한다면
                if data_from_queue == b'\x00\x00\x00\x03': #서버에서의 전송받을 시 공백구분데이터 > 이때는 패스
                    continue
                else:
                    #받은 데이터가 hangle 안에 있는 문자열 일 때
                    if data_from_queue.decode() in hangle:# !!!! data.decode() 는data유형을 실제로 변환시키지 않는다.
                        print('발신',data_from_queue.decode(),end='') #전송된 데이터와 유니티로의 전송이 성공했을때를 알려주는 디버깅용 함수
                        print(' >>> 유니티로 전송 발신 성공')
                        client_socket.send(data_from_queue) #실제 유니티로 데이터 전송
                        time.sleep(0.25)
                        
                    elif data_from_queue.decode() == ' ':
                        print('발신',data_from_queue.decode(),end='') #전송된 데이터와 유니티로의 전송이 성공했을때를 알려주는 디버깅용 함수
                        print(' >>> 유니티로 전송 발신 성공')
                        client_socket.send(data_from_queue) #실제 유니티로 데이터 전송
                        time.sleep(0.1)
            
        except ConnectionResetError as e:
            print('Disconnected by 유니티 예외처리')# 예외발생시 유니티와의 tcp연결 종료를 알리는 디벙깅용함수
            break
    
    print("유니티 클라이언트 접속 종료")
    client_socket.close() #클라이언트 연결 종료