import os

import numpy as np
import argparse

def readDirTxt(dirPath):
    if dirPath[-1] == '/':
        return
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            f = dirPath+'/'+f
            if os.path.isdir(f):
                subFiles = readDirTxt(f)
                allFiles = subFiles + allFiles #合并当前目录与子目录的所有文件路径
            elif f.split('.')[-1] == 'txt':
                allFiles.append(f)
            else:
                continue
        return allFiles
    else:
        return 'Error,not a dir'

def read_xml_list(file):
    file_list = []
    with open(file, 'r') as file_r:
        lines = file_r.readlines()
        for line in lines:
            value = line.strip()
            file_list.append(value)
    return file_list
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--labelimg-path', type=str, help='labelimg txt dir')
    parser.add_argument('--imglab-path', type=str, help='imglab txt dir')
    opt = parser.parse_args()

    # labels1=read_xml_list('/data/Rubby/data/20220714_test/1.txt')
    # labels2=read_xml_list('/data/Rubby/data/20220714_test/2.txt')

    labels1 = readDirTxt(opt.labelimg_path)
    labels2 = readDirTxt(opt.imglab_path)
    labels1.sort()
    labels2.sort()


    # labels1=read_xml_list(opt.labelimg_txt)
    # labels2=read_xml_list(opt.imglab_txt)

    save_dir = opt.labelimg_path.split('/')[-1]
    for i in range(len(labels1)):
        if os.path.split(labels1[i])[-1]==os.path.split(labels2[i])[-1]:
            with open(labels1[i], 'r') as f:
                lb1 = [x.split() for x in f.read().strip().splitlines()]  # labels
            with open(labels2[i], 'r') as f:
                lb2 = [x.split() for x in f.read().strip().splitlines()]
            lb1.extend(lb2)# labels

            label_path = labels1[i].replace(save_dir, 'labels_merge')
            base_path, basename = os.path.split(label_path)
            dst_path = base_path.replace(save_dir, 'labels_merge')

            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            with open(label_path, "w+", encoding='UTF-8') as out_file:
                for bb in lb1:
                    out_file.write( " ".join([str(a) for a in bb]) + '\n')
