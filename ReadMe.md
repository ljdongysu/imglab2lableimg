## Convert imglab's label to labelimg's 
### 转换imglab的xml标签到labelimg格式的xml
imglab 地址：https://github.com/NaturalIntelligence/imglab
lableimg 地址： https://github.com/liujiaxing7/labelImg
### 转换方式
--image-dir 对应包含全部图像的路径 imglab.xml为通过imglab保存的<Dlib XML>文件
python imglab_xml.py --image-dir /data/image --imglab-xml imglab.xml