import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import os
from pathlib import Path
from xml.etree import ElementTree  # 导入ElementTree模块
from get_dir_image import conver_list_dict, readDirImg
import argparse

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


def apped_obj(obj,obj_name,x,y,w,h):
    name = Element("name")
    name.text = obj_name
    pose = Element("pose")
    pose.text = "Unspecified"
    truncated = Element("truncated")
    truncated.text = "0"
    difficult = Element("difficult")
    difficult.text = "0"
    distance = Element("distance")
    distance.text = "0"
    obj.append(name)
    obj.append(pose)
    obj.append(truncated)
    obj.append(difficult)
    obj.append(distance)

    bndbox = ET.Element('bndbox')
    obj.append(bndbox)
    xmin = ET.Element('xmin')
    xmin.text = str(x)
    bndbox.append(xmin)
    ymin = ET.Element('ymin')
    ymin.text = str(y)
    bndbox.append(ymin)
    xmax = ET.Element('xmax')
    xmax.text = str(x + w)
    bndbox.append(xmax)
    ymax = ET.Element('ymax')
    ymax.text = str(y + h)
    bndbox.append(ymax)

def imglab2lableimg(imglab_xml, image_dict, img_dir):
    doc = ET.parse(imglab_xml)
    root = doc.getroot()
    print(root)

    images = root.find('images')
    print(images)

    image = images.findall('image')
    for file in image:
        filename = file.attrib['file']
        print("filename: ", filename)

        filename = filename.split('.')[0]

        new_root = ET.Element('annotation')
        new_tree = ET.ElementTree(new_root)

        new_folder = ET.Element('folder')
        print(filename)
        if filename not in image_dict.keys():
            continue
        print(image_dict)
        print(image_dict[filename])
        new_folder.text = image_dict[filename].split('/')[-2] #print("image_dict[filename]: " ,image_dict[filename].split('/')[-2])
        new_root.append(new_folder)

        new_filename = Element("filename")
        new_filename.text = filename
        new_root.append(new_filename)

        new_path = ET.Element('path')
        new_folder.text = image_dict[filename]
        print("image_dict[filename]: ", image_dict[filename])
        new_root.append(new_path)

        new_size = Element("size")
        new_root.append(new_size)

        new_width = Element("width")
        new_width.text = "640"
        new_height = Element("height")
        new_height.text = "400"
        new_depth = Element("depth")
        new_depth.text = "1"

        new_size.append(new_width)
        new_size.append(new_height)
        new_size.append(new_depth)

        img_abs_path = image_dict[filename]
        print("img_abs_path: ", img_abs_path)
        print("img_dir: ", img_dir)
        label_img_xml_suffix = img_abs_path[len(img_dir) :]
        print("label_img_xml_suffix: ", label_img_xml_suffix)

        label_img_xml = img_dir + "/ANNOTATIONS/" + label_img_xml_suffix
        label_img = label_img_xml.split(".")[0]
        label_img = label_img + ".xml"
        print("save label_img: ", label_img)
        label_img_dir = "/".join(label_img.split('/')[:-1])
        print("label_img_dir: ", label_img_dir)

        if  not os.path.exists(label_img_dir):
            os.makedirs(label_img_dir)

        box = file.findall('box')
        for box_a in box :
            print(box_a.attrib)
            y=int(box_a.attrib['top'])
            x=int(box_a.attrib['left'])
            w=int(box_a.attrib['width'])
            h=int(box_a.attrib['height'])
            print(x,y,w,h)

            label = box_a.find('label')
            if label.text == 'unlabelled_c':
                label.text = 'desk_circle'
            elif label.text == 'unlabelled':
                label.text = 'desk'
            print(label.text)

            new_object = Element('object')
            new_root.append(new_object)
            apped_obj(new_object,label.text,x,y,w,h)


            new_keyPoints = Element('keyPoints')
            new_object.append(new_keyPoints)

            part = box_a.findall('part')
            for part_a in part:
                print(part_a.attrib)
                new_Point = Element('Point')
                new_keyPoints.append(new_Point)
                new_Point.attrib = part_a.attrib



        pretty_xml(new_root,'\t','\n')

        print(label_img)
        new_tree.write(label_img,xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-dir', type=str, help='image dir')
    parser.add_argument('--imglab-xml', type=str, help='xml from imglab')
    opt = parser.parse_args()
    image_root_dir = opt.image_dir
    imglab_xml = opt.imglab_xml
    image_list = readDirImg(image_root_dir)
    print(image_list)
    image_dict = conver_list_dict(image_list)
    print(image_dict)
    imglab2lableimg(imglab_xml, image_dict, image_root_dir)
