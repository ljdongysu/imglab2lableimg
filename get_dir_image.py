import os
def readDirImg(dirPath):
    if dirPath[-1] == '/':
        return
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            f = dirPath+'/'+f
            if os.path.isdir(f):
                subFiles = readDirImg(f)
                allFiles = subFiles + allFiles #合并当前目录与子目录的所有文件路径
            elif f.split('.')[-1] == 'jpg' or f.split('.')[-1] == 'png':
                allFiles.append(f)
            else:
                continue
        return allFiles
    else:
        return 'Error,not a dir'

def conver_list_dict(image_list):
    image_dict = {}
    for image in image_list:
        image_key = image.split('/')[-1].split('.')[0]
        image_dict[image_key] = image
    return image_dict

if __name__ == '__main__':

    image = "/home/indemind/1/2/3/4/img.jpg"
    image1 = "/home/indemind/1/2"
    image2 = image.strip(image1)
    print(image2)
    assert 0
    image_list = readDirImg("/data/Rubby/data/data_desk_0_remap_filter")
    print(image_list)
    image_dict = conver_list_dict(image_list)
    print(image_dict)

    # os.makedirs("/home/indemind/abc/1.jpg")
    print(os.path.abspath("/home/indemind/abc/1.jpg"))
    a = "/home/indemind/abc/1.jpg"
    print(a)
    print("11", "/".join(a.split('/')[:-1]))

    # a = [1,2,3,4,5]
    # print(tuple(a[2:]))