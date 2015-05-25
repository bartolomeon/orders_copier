#!/usr/bin/env python

import os
import re
import lxml.etree
from ftplib import FTP
import config


def checkXMLFile(filePath):
    salesChannels = []
    try:
        tree = lxml.etree.parse(filePath)
        root = tree.getroot()

        # <order><sales_channel_code>CZECHY<
        salesChannels = root.xpath('./order/sales_channel_code/text()')
        print "Successfuly parsed file: " + filePath

    except Exception:
        print "Failed parsing file: " + filePath + " - skipping file."
        pass

    return salesChannels


def copyFileToFTP(fileName):
    print 'Copying file: ' + fileName + ' to FTP server...'
    ftp = FTP(config.ftp_host)
    ftp.login(config.ftp_user, config.ftp_password)
    ftp.cwd(config.ftp_dir)
    # `ftp.retrlines('LIST')

    f = open(os.path.join(config.source_dir, fileName), 'rb')
    ftp.storbinary('STOR ' + fileName, f, 1024)
    ftp.close()
    print 'File ' + fileName + ' transferred to FTP.'


def processFilesInDir(sourceDir):
    allXmlFiles = [f for f in os.listdir(config.source_dir) if re.match(r'.*\.xml$', f)]
    matchingFiles = [f for f in allXmlFiles if 'CZECHY' in checkXMLFile(os.path.join(config.source_dir, f))]

    for fileName in matchingFiles:
        copyFileToFTP(fileName)

print 'Starting...'
processFilesInDir(config.source_dir)
print 'Done.'
