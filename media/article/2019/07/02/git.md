title: git教程
tags:
  - git
categories:
  - back-end
comments: true
type: categories
author: ANT锟
date: 2019-06-19 16:11:00
---
#### git 配置
git 提供了一个叫做 git config 的工具，专门用来配置或读取相应的工作环境变量。

这些环境变量，决定了 Git 在各个环节的具体工作方式和行为。这些变量可以存放在以下三个不同的地方：

/etc/gitconfig 文件：系统中对所有用户都普遍适用的配置。若使用 git config 时用 --system 选项，读写的就是这个文件。
~/.gitconfig 文件：用户目录下的配置文件只适用于该用户。若使用 git config 时用 --global 选项，读写的就是这个文件。
当前项目的 Git 目录中的配置文件（也就是工作目录中的 .git/config 文件）：这里的配置仅仅针对当前项目有效。每一个级别的配置都会覆盖上层的相同配置，所以 .git/config 里的配置会覆盖 /etc/gitconfig 中的同名变量。
在 Windows 系统上，Git 会找寻用户主目录下的 .gitconfig 文件。主目录即 $HOME 变量指定的目录，一般都是 C:\Documents and Settings\$USER。

此外，Git 还会尝试找寻 /etc/gitconfig 文件，只不过看当初 Git 装在什么目录，就以此作为根目录来定位
<!-- more -->
#### 用户信息
配置个人的用户名称和电子邮件地址：

```bash
$ git config --global user.name "runoob"
$ git config --global user.email test@runoob.com
```

如果用了 --global 选项，那么更改的配置文件就是位于你用户主目录下的那个，以后你所有的项目都会默认使用这里配置的用户信息。

如果要在某个特定的项目中使用其他名字或者电邮，只要去掉 --global 选项重新配置即可，新的设定保存在当前项目的 .git/config 文件里。
#### 查看配置信息
```bash
git config --list
```
#### 常用命令
```bash
$ git init # 初始当前目录为git仓库目录
$ git init newgit # 初始newgit为git仓库目录
$ git add ./ # 添加git追踪
$ git commit -m '初始化项目版本' # 提交到本地仓库中
$ git clone [<repo>] [<directory>] # repo:Git 仓库。 directory:本地目录。克隆远程项目到本地目录
# git status # 命令用于查看项目的当前状态。
$ git reset HEAD filename # 撤销add的文件到未add状态
git rm # 删除已经commit的文件
	-r # 递归删除
	-f # commit后经过修改，包括add前后都可以
   --cached # 和-f相比，当前目录还存在这个文件
git mv README  README.md # 重命名文件，git是先删除，再创建一个一样的文件，但名字不同
git branch # 列出分支
	branchname # 新建分支
git checkout 
	branchname # 切换分支
   		-b # 新建并切换到新分支
      -d # 删除分支
git merge newtest -m "message" # 将newtest分支合并到当前分支    
git log # 查看历史提交记录
	--oneline # 查看简单版历史记录
   --graph # 查看历史中什么时候出现了分支、合并
   --reverse # 逆向显示所有日志。
   --author=name # 查找指定用户的提交日志
   
git fetch origin master:tmp 
#在本地新建一个temp分支，并将远程origin仓库的master分支代码下载到本地temp分支
git diff tmp 
#来比较本地代码与刚刚从远程下载下来的代码的区别
git merge tmp
#合并temp分支到本地的master分支
git branch -d temp
#如果不想保留temp分支 可以用这步删除
```