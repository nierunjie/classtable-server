# 微信课程表server端

使用该网页获取课程表微信小程序剪切板所需的信息

微信小程序源码[在这里](https://github.com/nierunjie/classtable-client)

## 目前支持的学校列表
* 山东农业大学
* 泰山医学院

## 如何参与

爬虫相关操作均在 *registrar* 目录下.

根据实际情况选择性的实现 *class Registrar* 中的方法.

## 规范
目前按以下规范,若有更好的建议请提issue.

> 以**小写**的学校名缩写为文件名.如 *urp.py*
> 
> 以**全部大写**的学校名为类名,继承Registrar.如class URP(registrar.Registrar)

## 许可证

> GPL-3.0
