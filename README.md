# mobile_URL_extract
移动安全 URL 提取工具 
#### 依赖:
python3，baksmali，apktool，strings

#### 使用:
python3 ./main.py -a/i targetFilePath

-a/i targetFilePath(目标apk/ipa/dex/ios可执行文件/目录)

-a android

-i ios

-h help

#### 例如:
python main.py -a Tomato.apk

#### 注意:
使用之前 请配置basksmali和apktool的路径（默认为当前路径）
