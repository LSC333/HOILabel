### windows10+python3.6


HOILabel是一个HOI的标注工具，它在通过预先标注好的目标检测的标注文件进行标注，即在使用HOILabel进行HOI的标注之前需要先进行目标检测的标注，在得到(voc或yolo)格式的标注文件之后，再进行HOI的标注。
* 安装项目依赖
>pip install -r requirements.txt

* 快捷键
> next:D
> prev:A
> save:Ctrl+S
> combine:Ctrl+W
> quit:Ctrl+Q

* 如何使用
    * 将目标类别文件（classes.txt）和交互文件(interaction.txt)放在目录的*dataFile*下
    * 运行*HOILabel.py*
    * 选择图片文件、标注文件、json存储的路径以及标注文件的格式

* 注意事项
    * 在标注完一张图片之后，要记得保存，否则切换到下一张图片后会丢失这张的标注信息
    * 注意标注文件的格式(voc或yolo)，不同的格式需要切换对应的按钮
    * 如果图片所对应的标注文件不存在就只会显示这张图片，并且无法给这张图片添加HOI的标注
