import socket 
import json 

# UDP 소켓 설정
HOST = "127.0.0.1"  # 서버 주소 (로컬 테스트)
PORT = 5005  # 서버 포트
BUFFER_SIZE = 8192  # 버퍼 사이즈

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 소켓 설정
sock.bind((HOST, PORT))  # 소켓 바인딩

print("🚀 서버 실행 중...")

while True:
    try:
        # JSON 길이가 너무 길어서 여러 번 나눠서 받음
        received_data = ""
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            part = data.decode("utf-8")
            received_data += part
            if part.endswith("END"):  # ✅ "END"가 오면 데이터 수신 완료
                received_data = received_data[:-3]  # "END" 제거
                break

        # ✅ JSON 변환
        json_data = json.loads(received_data)
        print(f"📩 JSON 파싱 성공: {json_data}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

sock.close()