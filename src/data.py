# Copyright 2004 Troy Potts et al.  All rights reserved.

import ika
import config
import ariesparser as parser

enemyData = None
enemyNames = None
itemData = None
itemNames = None
itemIcons = {}
skillData = None
skillNames = None

def init():
    global enemyData, enemyNames, itemData, itemNames, itemIcons, skillData, skillNames
    enemyData, enemyNames = readDataFile("enemies.cfg", "enemy", "sprite")
    itemData, itemNames = readDataFile("items.cfg", "item")
    for i in itemData.values():
        itemIcons[i['name']] = ika.Image('%s/items/%s' % (config.IMAGE_PATH, i.get('icon', 'icon_seashell.png')))
    #skillData, skillNames = readDataFile("skills.cfg", "skill")

def readDataFile(fileName, nodeName, keyAttrib="name"):
    data = parser.Document('%s/%s' % (config.DATA_PATH, fileName)).process()
    dataSet = {}
    nameList = []

    for node in data:
        if node.name == nodeName:
            dataEntry = node.toDict(flat=False)
            assert keyAttrib in dataEntry, "No such attribute '%s'" % (keyAttrib)
            assert dataEntry[keyAttrib] not in dataSet, "Duplicate %s with name '%s'" % (nodeName, dataEntry['name'])
            dataSet[dataEntry[keyAttrib]] = dataEntry
            nameList.append(dataEntry[keyAttrib])
    return dataSet, nameList