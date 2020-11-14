import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
from PySide2 import QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QComboBox
from util.img import loadImg
from util.img import labelImgVOC, labelImgYOLO
from util.ioTXT import readTxT
from util.ioJSON import saveJSON, combineJSON

'''
shortcut:
    next:D
    prev:A
    save:Ctrl+S
    combine:Ctrl+W
    quit:Ctrl+Q
'''


class HOILabel:
    def __init__(self):

        self.ui = QUiLoader().load('ui/HOILabel.ui')
        self.imgPath = ''
        self.labelPath = ''
        self.imgList = []
        self.index = 0
        self.labels = []
        self.interaction = readTxT('dataFile/interaction.txt')
        self.classes = readTxT('dataFile/classes.txt')
        self.jsonPath = ''
        self.voc = 1

        # button action
        self.ui.imgDir.clicked.connect(self.action_imgDir)
        self.ui.labelDir.clicked.connect(self.action_labelDir)
        self.ui.jsonDir.clicked.connect(self.action_jsonDir)
        self.ui.save.clicked.connect(self.action_save)
        self.ui.next.clicked.connect(self.action_next)
        self.ui.prev.clicked.connect(self.action_prev)
        self.ui.combine.clicked.connect(self.action_combine)
        self.ui.addRow.clicked.connect(self.action_addRow)
        self.ui.delRow.clicked.connect(self.action_delRow)
        self.ui.voc.clicked.connect(self.action_voc)
        self.ui.quit.clicked.connect(QCoreApplication.quit)

        self.ui.imgList.doubleClicked.connect(self.imgListDoubleClicked)

    def action_voc(self):
        self.voc ^= 1
        if self.voc:
            self.ui.voc.setText('voc')
        else:
            self.ui.voc.setText('yolo')

    def action_combine(self):
        combineJSON(self.jsonPath)

    def action_jsonDir(self):
        tmpPath = QFileDialog.getExistingDirectory(self.ui, "请选择json文件保存路径",
                                                   r".")
        if tmpPath:
            self.jsonPath = tmpPath + '/'

    def action_addRow(self):
        if not self.labels:
            return
        self.ui.HOIList.insertRow(0)
        ids = [str(i) for i in range(len(self.labels))]
        for i in range(2):
            comBox = QComboBox()
            comBox.addItems(ids)
            self.ui.HOIList.setCellWidget(0, i, comBox)
        comBox = QComboBox()
        comBox.addItems(self.interaction)
        self.ui.HOIList.setCellWidget(0, 2, comBox)

    def action_delRow(self):
        currentRow = max(0, self.ui.HOIList.currentRow())
        self.ui.HOIList.removeRow(currentRow)

    def action_labelDir(self):
        tmpPath = QFileDialog.getExistingDirectory(self.ui, "请选择标注文件夹路径",
                                                   r".")
        if tmpPath:
            self.labelPath = tmpPath + '/'

    def action_prev(self):
        self.index = max(self.index - 1, 0)
        self.ui.HOIList.clearContents()
        self.ui.HOIList.setRowCount(0)
        self.labels = []
        self.imgShow()

    def action_next(self):
        self.index = min(self.index + 1, len(self.imgList) - 1)
        self.ui.HOIList.clearContents()
        self.ui.HOIList.setRowCount(0)
        self.labels = []
        self.imgShow()

    def action_imgDir(self):

        tmpPath = QFileDialog.getExistingDirectory(self.ui, "请选择图片文件夹路径",
                                                   r".")
        if tmpPath:
            self.imgPath = tmpPath + '/'
        # print(self.imgPath)
        self.imgList = os.listdir(self.imgPath)
        self.index = 0
        self.ui.imgList.addItems([self.imgPath + img for img in self.imgList])
        # print(self.imgList)
        self.imgShow()

    def action_save(self):
        if not self.labels:
            return
        HOIDict = {'file_name': self.imgList[self.index], 'hoi_annotation': [], 'annotations': []}
        rowCount = self.ui.HOIList.rowCount()
        for i in range(rowCount):
            subjectID = int(self.ui.HOIList.cellWidget(i, 0).currentText())
            objectID = int(self.ui.HOIList.cellWidget(i, 1).currentText())
            interaction = self.ui.HOIList.cellWidget(i, 2).currentText()
            hoiAnnotation = {'subject_id': subjectID, 'object_id': objectID,
                             'category_id': self.interaction.index(interaction)}
            HOIDict['hoi_annotation'].append(hoiAnnotation)
        for label in self.labels:
            bbox = label['bbox']
            categoryID = self.classes.index(label['name'])
            annotation = {'bbox': label['bbox'], 'category_id': categoryID}
            HOIDict['annotations'].append(annotation)
        saveJSON(self.jsonPath + self.imgList[self.index].split('.')[0] + '.json', HOIDict)

    def imgShow(self):
        if not self.labelPath or \
                not (os.path.exists(self.labelPath + self.imgList[self.index].split('.')[0] + '.xml') or
                     os.path.exists(self.labelPath + self.imgList[self.index].split('.')[0] + '.txt')):
            img = loadImg(self.imgPath + self.imgList[self.index], self.ui.img.width(),
                          self.ui.img.height())
            image = QtGui.QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)
            imgOut = QtGui.QPixmap(image)
            self.ui.img.setPixmap(imgOut)
        else:
            if self.voc:
                img, self.labels = labelImgVOC(self.imgPath + self.imgList[self.index],
                                               self.labelPath + self.imgList[self.index].split('.')[0] + '.xml',
                                               self.ui.img.width(),
                                               self.ui.img.height())
            else:
                img, self.labels = labelImgYOLO(self.imgPath + self.imgList[self.index],
                                                self.labelPath + self.imgList[self.index].split('.')[0] + '.txt',
                                                self.ui.img.width(),
                                                self.ui.img.height(), self.classes)
            image = QtGui.QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)
            imgOut = QtGui.QPixmap(image)
            self.ui.img.setPixmap(imgOut)

        self.ui.imgList.setCurrentRow(self.index)

    def imgListDoubleClicked(self):
        img = self.ui.imgList.currentItem().text().split('/')[-1]
        self.index = self.imgList.index(img)
        self.imgShow()


if __name__ == "__main__":
    app = QApplication([])
    hoiLabel = HOILabel()
    hoiLabel.ui.show()
    app.exec_()
