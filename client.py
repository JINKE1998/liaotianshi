from socket import *
import os,sys


#创建套接字，登录，创建子进程
def main():

    if len(sys.argv) < 3:
        print('argv is error')
        return 
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    s = socket(AF_INET,SOCK_DGRAM)


    while True:
        name = input('请输入姓名：')
        msg = 'L '+name
        #发送登录请求
        s.sendto(msg.encode(),ADDR)

        #等待服务器回复
        data,addr=s.recvfrom(1024)
        if data.decode() == 'ok':
            print('您已进入聊天室')
            break
        else:
            #不成功服务器服务器回复不允许登录原因
            print(data.decode())

    #创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit('创建进程失败')

    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)


#发送消息
def send_msg(s,name,addr):
    while True:
        text = input('发言：')
        #如果输入quit退出
        if text.strip() == 'quit':
            msg='Q '+name
            s.sendto(msg.encode(),addr)
            sys.exit('退出聊天室')
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

#接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode()+'\n发言：',end='')




if __name__ == '__main__':
    main()