import os, requests

default_path = 'data/'

def PathMaker(path): #make path if not exist

    if os.path.exists(path):
        i = 2
        while True:
            path_list = path.split('/')
            if path_list[-1]== "":
                path_list[-2] = path_list[-2] + str(i)
                temp_path = "/".join(path_list)
            else:
                path_list[-1] = path_list[-1] + str(i)
                temp_path = "/".join(path_list)+"/"
            if not os.path.exists(temp_path):
                break
            i+=1
        path = temp_path
    path_list = path.split('/')

    for a in range(0, len(path_list)):
        sub_path = ""
        for i in range(0, a + 1):
            sub_path += path_list[i] + "/"
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
    print("path made:"+path)
    return path

def DownloadImage(src, filename = None, path=default_path):
    if not filename:
        filename = src.split('/')[-1].split('?')[0]
    file_path = path+filename
    f = open(file_path, 'wb')
    f.write(requests.get(src).content)
    f.close()
