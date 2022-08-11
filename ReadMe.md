## Convert imglab's label to labelimg's And merge two tools' txt file 
## 转换imglab和labelimg的xml到txt并且合并两个txt文件，imglab标注的文件包含关键点
### 转换imglab的xml标签到labelimg格式的xml
imglab 地址：https://github.com/NaturalIntelligence/imglab  
lableimg 地址： https://github.com/liujiaxing7/labelImg
## 转换方式
### imglab 的xml转为labelimg的xml
`````--image-dir````` 对应包含全部图像的路径 ```imglab.xml```为通过imglab保存的```Dlib XML```文件 , 会在--image-dir 路径下生成```ANNOTATIONS```文件夹，包含着全部的单个图像对应的xml文件  
运行代码： ```python imglab_xml.py --image-dir /data/image --imglab-xml imglab.xml```  

### imglab和labelimg的xml转为txt
 - imglab的xml转txt
   - 运行代码： ```python imglab2xml.py  --root-path ANNOTATIONS  --xml-list  imglab_xml.txt```
   - ```ANNOTATIONS``` 为上一步骤生成的包含单个图像xml文件夹的路径，```imglab_xml.txt```为每个xml文件列表， 运行后会自动在```ANNOTATIONS```同级目录生成```labels_imglab```目录保存txt文件
 - labelimg的xml转txt
   - 运行代码： ```python lableimg2txt.py  --root-path ANNOTATIONS  --xml-list  imglab_xml.txt```
   - ```ANNOTATIONS```为labelimg标注的xml文件夹，`imglab_xml.txt`为xml文件列表,运行后会自动在```ANNOTATIONS```同级目录生成```labels_labelimg```目录保存txt文件
   
### 合并两个txt
 - 合并两个txt
 - 运行代码： ```python txt_merge.py --labelimg-path labels_labelimg--imglab-path  labels_imglab ```
 - 会在```labels_labelimg```同级目录下生成新的合并后文件夹```labels_merge```
