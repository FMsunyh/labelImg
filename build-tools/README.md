cd G:\labelImg\build-tools\pyinstaller
python setup.py install

cd G:\labelImg\build-tools

activate label_pyinstaller2.7
pyrcc4 -o resources.py resources.qrc
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../


build：2018-11-02
activate label_pyinstaller
cd cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v.1.8.0 -c "../labelImg.py" -p ../libs -p ../
