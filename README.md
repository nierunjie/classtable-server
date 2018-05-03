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
以**小写**的学校名缩写为文件名.如 *urp.py*
以**全部大写**的学校名为类名,继承Registrar.如class URP(registrar.Registrar)

## 许可证

> Copyright 2018 Ya
> 
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
> 
>     http://www.apache.org/licenses/LICENSE-2.0
> 
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
