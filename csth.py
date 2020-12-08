#!/usr/bin/python
import paramiko
import os

#当前脚本路径
CUR_PATH = os.path.dirname(__file__)

#服务器ip
Host='47.110.231.19'
Port=22
#登录用户名
Username='root'
#登录密码
Password='Jayking0216'
#登录服务器后执行的命令
Command = ['cd /usr/ESandTable/web/web-resource/web/cchj; rm -rf *']
Command_tar = ['cd /usr/ESandTable/web/web-resource/web/cchj; tar -vxf h5demo.tar']
#本地PC路径
WinPath = CUR_PATH + '\\h5demo.tar'
#服务器上的路径
LinuxPath = '/usr/ESandTable/web/web-resource/web/cchj/h5demo.tar'

def ssh_exec_cmd(command):
    '''SSHA远程登录：Windows客户端连接Linux服务器，并输入指令'''

    #登录服务器
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, Port, Username, Password)

    #执行命令
    for i in range(len(command)):
        send_str = command[i] + '\n'
        stdin, stdout, stderr = ssh.exec_command(send_str)
        err = stderr.readlines()
        out = stdout.readlines()
        if (err):
            print ('error:')
            print (err)
            #print (out)
        else:
            print (out)

    #执行完毕，终止连接
    ssh.close()
    
    
def ssh_linux_to_win(linuxpath, winpath):
    '''从Linux服务器下载文件到本地

    Args:
        linuxpath: 文件在服务器上的路径及名字
        winpath: 文件下载到本地的路径及名字

    '''

    client = paramiko.Transport((Host, Port))
    client.connect(username=Username, password=Password)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.get(linuxpath, winpath)
    client.close()
    print ('下载完成！')

def ssh_win_to_linux(winpath, linuxpath):
    '''从windows向linux服务器上传文件

    Args:
        winpath: 要上传的文件在本地的路径及位置
        linuxpath: 文件要上传至服务器的路径及名字
    '''

    client = paramiko.Transport((Host, Port))
    client.connect(username=Username, password=Password)
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.put(winpath, linuxpath)
    client.close()
    print ('上传完成!')


if __name__=='__main__':
    ssh_exec_cmd(Command)                   #清空文件
    ssh_win_to_linux(WinPath, LinuxPath)    #上传文件
    ssh_exec_cmd(Command_tar)               #解压文件