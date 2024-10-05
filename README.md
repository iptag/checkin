请勿fork，点亮star即可，不会跑路滴~！


转载自https://github.com/OreosLab/checkinpanel

感谢Oreo大佬基于青龙的架构！！

出于自用精简的目的删除掉部分用不上的功能，注意：不支持v2p

通知模块采用的sendNotify.js和sendNotify.py，跟jd相同

1.修改config.sh


RepoFileExtensions="js pl py sh ts"

2.拉库


ql repo https://github.com/iptag/checkin.git "api_|ck_|ins_" "^checkin" "^sendNotify|^utils|cpm|^jsencrypt" "main"

3.运行 签到依赖 任务

4.复制check.sample.toml到config目录下，文件名改成check.toml，参考check.sample.toml的格式，在check.toml中添加上对应脚本的cookie或相关数据，有些脚本因为失效已删除，但check.toml仍然保留，不用管它
