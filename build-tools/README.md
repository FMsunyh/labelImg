cd G:\labelImg\build-tools\pyinstaller
python setup.py install

cd G:\labelImg\build-tools

activate label_pyinstaller2.7
pyrcc4 -o resources.py resources.qrc
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../


build：2018-11-02
version：labelImg_v.1.8.0

activate label_pyinstaller
cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v.1.8.0 -c "../labelImg.py" -p ../libs -p ../


build：2018-11-09
修改：添加删除操作，删除不合格图片
version：labelImg_v.1.9.0

activate label_pyinstaller
cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v.1.9.0 -c "../labelImg.py" -p ../libs -p ../


build：2018-11-13
修复：同时，保留 RectBox 删除操作，删除图片操作
version：labelImg_v.2.0.0

activate label_pyinstaller
cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v.2.0.0 -c "../labelImg.py" -p ../libs -p ../


build：2019-06-10
增强：可视化，增大矩形框和圆点。
version：labelImg_v.2.6.0

activate label_pyinstaller
cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v2.6.0 -c "../labelImg.py" -p ../libs -p ../

不在使用这个文件的说明
因为编译出来的exe，在win7上无法使用。