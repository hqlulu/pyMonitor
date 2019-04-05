我们来一个不断进阶的fpm监控任务，熟悉python脚本的编写。

首先我们确定一下fpm可以怎么监控：
1. fpm需要开放一个固定的地址，返回进程信息
2. nginx代理此地址
3. 监控进程访问nginx获取
4. 汇总到ElasticSearch，可以做图看进程数变化

php-fpm.d/www.conf 的配置，取消前面默认的";"即可，重启fpm生效
```
pm.status_path = /status
```

nginx配置：
```
server {
    listen       80;
    server_name  fpm9000;
    root /tmp;
    index index.php index.html index.htm;

    location /status {
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;

        fastcgi_split_path_info  ^(.+\.php)(/.*)$;
        fastcgi_param  PATH_INFO $fastcgi_path_info;

        include        fastcgi.conf;
    }
}
```

nginx所在的服务器核验一下：
```
curl -H "host:fpm9000" localhost/status
pool:                 www
process manager:      dynamic
start time:           30/Mar/2019:15:27:36 +0800
start since:          493473
accepted conn:        59477
listen queue:         0
max listen queue:     129
listen queue len:     128
idle processes:       353
active processes:     1
total processes:      354
max active processes: 349
max children reached: 0
slow requests:        0
```

fpm监控支持json输出
```
curl -H "host:fpm9000" "localhost/status?json"
{"pool":"www","process manager":"dynamic","start time":1553930856,"start since":493566,"accepted conn":59479,"listen queue":0,"max listen queue":129,"listen queue len":128,"idle processes":353,"active processes":1,"total processes":354,"max active processes":349,"max children reached":0,"slow requests":0}
```

## screen shoots

![image](https://raw.githubusercontent.com/hqlulu/pyMonitor/master/screen_shoot/screen_shoot_es_detail.png)

![image](https://raw.githubusercontent.com/hqlulu/pyMonitor/master/screen_shoot/screen_shoot_es_visualize.png)
