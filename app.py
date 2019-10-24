from flask import Flask, render_template, request
from decouple import config
import requests,random

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')

# 텔레그램 서버가 우리 서버에게 HTTP POST 요청을 통해,
# 사용자 메시지 정보를 받아라고 전달해주는 것
# 우리가 status 200을 리턴해줘야 텔레그램 측이 더이상의 전송을 중단한다.
# 200을 안돌려주면 계속~~ POST 요청을 여러번 보낸다.
@app.route(f'/{token}', methods=['POST'])
def telegram():
    # 1. 메아리(Echo) 기능
    # 1.1 request.get.json() 구조 확인하기
    # print("이것 : ", request.get_json())
    # 1.2 [실습] 사용자 아이디, 텍스트 가져오기
    print(request.get_json())
    chat_id = request.get_json().get('message').get('from').get('id')
    text = request.get_json().get('message').get('text')

    if text == '/로또':
        lottonum=random.sample(range(1,46),6)
        lottonum.sort()
        text = "추천번호는 " + str(lottonum) + " 당첨되면 이몸에게 나눠줄 것"

    text2 = text[0:7]
    text3 = text[7:len(text)+1]
    text3.replace(" ","")
    if text2 == '/vonvon':
        # 2. 사용자에게 보여줄 여러가지 재미있는 특성들 리스트를 만든다.
        first_list = ['매우못생김', '못생김', '서혁진얼굴', '머존잘', '우주꼴등얼굴', '꼼장어', '오징어외모', '배추김치얼굴']
        second_list = ['자신감','귀찮음','쑥스러움','열정적임','하찮음']
        third_list = ['허세','물욕','식욕','똘기','폭풍섹시']

        # 3. 리스트에서 랜덤으로 하나씩을 선택한다.
        first = random.choice(first_list)
        second = random.choice(second_list)
        third = random.choice(third_list)
        print(text3[0])
        text = "신이 [" + text3 + "]를 만들 떄 [" + first + "]한 스푼, [" + second + "] 두 스푼, [" + third + "] 와장창창 넣어 만들었따리"
        
    # 1.3 [실습] 텔레그램 API에게 요청을 보내서 답변해주기
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

    # 1. [기본] 로또 기능
    #       사용자가 '/로또'라고 말하면 랜덤으로 번호 6개 뽑아서 돌려주기!
    #       나머지 경우엔 전부다 메아리 칩시다.

    # 2. [심화] vonvon 기능
    #       사용자가 '/vonvon 이름' 이라고 말하면 신이 나를 만들었을 때 요소 돌려주기!

    


    return '', 200











@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    text = request.args.get('message')
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return '<h1>메시지 전송 완료!</h1>'


if __name__ == '__main__':
    app.run(debug=True)