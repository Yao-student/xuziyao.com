# xuziyao.com

## 介绍

我的个人网站。使用 [Django](https://www.djangoproject.com/) Web 框架开发。
源码中保密内容已被隐藏，文件被添加至 [.gitignore](../.gitignore)，文件内字符被替换为 `secret`。

## 更新日志

### v2.2.0 (2025.09.18)

- [Notanote 查分器](http://xuziyao.com/notanote/rank/) 同步 v2.5.1 更新，并修复 bug
- 祝我自己 15 岁生日快乐！
- 其他小更改

### v2.1.2 (2025.08.18)

- [Notanote 查分器](http://xuziyao.com/notanote/best/) 与 [Notanote Rank 计算](http://xuziyao.com/notanote/rank/) 同步 v2.5.0 更新

### v2.1.1 (2025.08.12)

- 修复了 [Notanote Rank 计算](http://xuziyao.com/notanote/rank/) 提交时出现错误的问题

### v2.1.0 (2025.07.22)

- 修复了 [Phira 谱面文件下载](http://xuziyao.com/phira/download/) 无法正确下载谱面的问题
- [Notanote 查分器](http://xuziyao.com/notanote/best/) 同步 v2.4.0 更新
- [Notanote 单曲 Rank 计算](http://xuziyao.com/notanote/rank/) 更名为 [Notanote Rank 计算](http://xuziyao.com/notanote/rank/)
- [首页](http://xuziyao.com/) 增加新友情链接
- 其他小更改

### v2.0.0 (2025.07.14)

- 在页面底部显示网站运行天数与备案信息
- 增加 [更新日志](http://xuziyao.com/changelog/)
- [自制谱](http://xuziyao.com/fanmade_charts/)、[Phira 工具](http://xuziyao.com/phira/)、[PhiZone 工具](http://xuziyao.com/phizone/)、[Notanote 工具](http://xuziyao.com/notanote/) 页面上的无序列表链接改为卡片
- [PhiZone B27 计算](http://xuziyao.com/notanote/best/) 更名为 [PhiZone 查分器](http://xuziyao.com/phizone/best/)，修复了 Phi3 排版错误的问题
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 更名为 [Notanote 查分器](http://xuziyao.com/notanote/best/)，将查分方式改为更方便的上传成绩文件
- [Notanote 单曲 Rank 计算](http://xuziyao.com/notanote/rank/) URL 由 /notanote/rankcalc/ 改为 /notanote/rank/
- [编程](http://xuziyao.com/programming/) 板块更新文章
- [帖子](http://xuziyao.com/programming/) 板块更新
- 增加 [特别感谢](http://xuziyao.com/special_thanks/) 页面
- 优化了代码
- 其他小更改

### v1.2.5 (2025.06.28)

- 修复了 [自制谱](http://xuziyao.com/fanmade_charts/) 板块无法正确下载谱面的问题

### v1.2.4 (2025.06.22)

- [Phigros 自制谱](http://xuziyao.com/fanmade_charts/phigros/) 板块更新
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 同步 Notanote v2.3.0 更新

### v1.2.3 (2025.05.30)

- 将网页计数器从 [不蒜子](https://busuanzi.ibruce.info/) 改为 [Vercount](https://vercount.one/)
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 同步 Notanote v2.2.0 更新
- 增加新友情链接
- 其他小更改

### v1.2.2 (2025.05.24)

- 在页面底部显示访问量与访客量
- [PhiZone B27 计算](http://xuziyao.com/phizone/best/) 同步 PhiZone 更新，将 Phi1 + B19 改为 Phi3 + B27
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 分数前面自动补 0
- 其他小更改

### v1.2.1 (2025.05.04)

- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 同步 Notanote v2.1.1 更新

### v1.2.0 (2025.04.26)

- UI 部分更改
- 日记板块更名为 [帖子](http://xuziyao.com/posts/)
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 同步 Notanote v2.1.0 更新

### v1.1.2 (2025.04.20)

- UI 小更改
- [Phigros 自制谱](http://xuziyao.com/fanmade_charts/phigros/) 板块更新
- 其他小更改

### v1.1.1 (2025.04.12)

- 修复了当 B26 未被填满时 Nrk 计算错误的问题
- 其他小更改

### v1.1.0 (2025.03.31)

- 增加 [自制谱](http://xuziyao.com/fanmade_charts/) 板块
- 首页增加友情链接
- 增加面包屑导航
- [Notanote B26 计算](http://xuziyao.com/notanote/best/) 与 [Notanote 单曲 Rank 计算](http://xuziyao.com/notanote/rankcal/) 同步 Notanote v2.0.0 更新，改用新公式，使用 v1.7.0 公式的版本被迁移到 [Notanote B21 计算（v1.7.0）](http://xuziyao.com/notanote/best/v1.7.0) 与 [Notanote 单曲 Rank 计算](http://xuziyao.com/notanote/rankcal/v1.7.0)。数据格式中增加分数信息（选填），移除定数信息，输出结果中不同难度改用不同颜色。修复了当准确率全为 0 时发生错误的问题
- 增加置顶日记与置顶编程文章
- [编程](http://xuziyao.com/programming/) 板块更新文章
- 优化代码并修复错误
- 其他小更改

### v1.0.0 (2025.03.15)

- 上线网站
