import xml.etree.ElementTree as ET
import  os

def change_xml(xml_path):
    filelist = os.listdir(xml_path)
    print(filelist)
    # 打开xml文档
    for xmlfile in filelist:
        doc = ET.parse(xml_path + xmlfile)
        root = doc.getroot()
        sub1 = root.find('name')  # 找到filename标签，
        sub1.text = xmlfile  # 修改标签内容

        doc.write(xml_path + xmlfile)  # 保存修改

