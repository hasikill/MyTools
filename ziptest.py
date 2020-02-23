# coding:utf-8
import os
import zipfile

def unZipFile(unZipSrc,targeDir):
    if not os.path.isfile(unZipSrc):
        raise Exception('unZipSrc not exists:{0}'.format(unZipSrc))

    if not os.path.isdir(targeDir):
        os.makedirs(targeDir)

    print(u'开始解压缩文件:{0}'.format(unZipSrc))

    unZf = zipfile.ZipFile(unZipSrc,'r')

    for name in unZf.namelist() :
        unZfTarge = os.path.join(targeDir,name)

        if unZfTarge.endswith("/"):
            #empty dir
            splitDir = unZfTarge[:-1]
            if not os.path.exists(splitDir):
                os.makedirs(splitDir)
        else:
            splitDir,_ = os.path.split(targeDir)

            if not os.path.exists(splitDir):
                os.makedirs(splitDir)

            hFile = open(unZfTarge,'wb')
            hFile.write(unZf.read(name))
            hFile.close()
    print(u'解压缩完毕，目标文件目录:{0}'.format(targeDir))
    unZf.close()


cmd = "7z x ./download/OllyICE_1.10.rar -oapp/OllyICE_1.10 -aoa"

# unRarFile("./download/OllyICE_1.10.rar", "./app/OllyICE_1.10")
os.system(cmd)