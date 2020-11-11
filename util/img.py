import cv2
import xml.etree.ElementTree as ET


def loadImg(imgPath, width, height):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def labelImg(imgPath, labelPath, width, height):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    tree = ET.parse(labelPath)
    labels = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        labels.append(obj_struct)
    for i in range(len(labels)):
        cv2.rectangle(img, (labels[i]['bbox'][0], labels[i]['bbox'][1]),
                      (labels[i]['bbox'][2], labels[i]['bbox'][3]), (0, 0, 255), 2)
        cv2.putText(img, str(i), (labels[i]['bbox'][0], labels[i]['bbox'][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    return img, labels
