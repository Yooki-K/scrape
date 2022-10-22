/**
 * 
 * @authors KuangYu (1486147017@qq.com)
 * @date    2021-09-11 15:56:39
 * @version $Id$
 */

var https = require('https');
var tool = require('./core_bili.js')
var args = process.argv.splice(2)
const fs = require("fs"); //文件模块
const path = require("path"); //系统路径模块

//指定创建目录及文件名称，__dirname为执行当前js文件的目录
const file = path.join(args[0], "biliDM_"+args[1]+"_"+args[2]+".json");
let DATA = [];
(function myRequest(i){
    var url = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid='+args[1]+'&pid='+args[2]+'&segment_index='+i;
    var request = https.request(url, (response) => {
        let data = null;
        response.on('data', (chunk) => {
            if (data == null)
                data = Buffer.from(chunk);
            else{
                var temp = Buffer.from(chunk);
                data = Buffer.concat([data, temp], (data.length + temp.length));
            }

        });
        response.on('end', () => {
            // const body = JSON.parse(data);
            var content = tool.run(data)
//            var content = JSON.stringify(m, null, "\t");
//            content = JSON.parse(content)
            if (content['elems'].length != 0){
                DATA = DATA.concat(content['elems'])
                myRequest(i+1)
            }else{
                //写入文件
                fs.writeFile(file, JSON.stringify(DATA, null, "\t"), function (err) {
                  if (err) {
                    console.log('write error');
                    console.log(err);
                  }
                  console.log('success');
                  console.log(file);
                });
            }
        });
    })
    request.on('error', (error) => {
        console.log('scrape error');
        console.log(error)
    });
    request.end()
//    })

}(1))
//while (true){

//}
