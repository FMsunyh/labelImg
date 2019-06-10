# 创建打包环境
```bash
conda create -n label_pyinstaller2.7 python=2.7.13
activate label_pyinstaller2.7
pip install -r requirements.txt
conda install pyqt=4
conda install lxml
```


activate label_pyinstaller2.7
cd G:\labelImg\
pyrcc4 -py3 -o resources.py resources.qrc

cd G:\labelImg\build-tools
pyinstaller --hidden-import=xml  --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree  -D -F -n labelImg_v2.6.2 -c "../labelImg.py" -p ../libs -p ../
