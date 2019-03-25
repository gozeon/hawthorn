# 背景

> 星星只有在夜里才璀璨夺目啊。

我司前端编译主要有两个平台：[mis](http://mis.jiedaibao.com/) 和 [JDBuild](http://wiki.jdb-dev.com/pages/viewpage.action?pageId=49190604)。

## 关于 Mis

[mis](http://mis.jiedaibao.com/) 平台主要功能是编译、路由管理、日志、上线(Jira)等，是一个完备的系统。他存在一个弊端或者说 bug (*此处仅针对编译来说*)，是编译功能和 server 在同一台机器，启动编译使用 `node script` 的方式。这样的方式会带来以下问题：

- 环境问题
- 性能问题

### 环境问题

对于 node 开发者来说，node 环境问题是很头疼的。虽然社区有很多管理工具，比如 [nvm](https://github.com/creationix/nvm)，[yarn](https://yarnpkg.com/en/) 。但还是无法解决一些隐藏的弊端。举一个很常见的例子，[nvm](https://github.com/creationix/nvm) 切换 node 版本使用时，npm 版本也会更改，但是 `~/.npm/` 下的文件缓存的东西是不会更改的，这样就给我们带来一些校验、版本不一致的问题，从而导致编译失败或编译结果出现问题。[mis](http://mis.jiedaibao.com/) 本地编译的方式，随着项目种类的增多、技术的更新迭代，环境问题越来越明显，不少项目需要管理员登录到服务器手动删除`node_modules`或制定版本等操作。由于一些历史原因，[mis](http://mis.jiedaibao.com/) 服务器成了特定的编译环境(*比如：ngu*)，耦合性及其强。

### 性能问题

[mis](http://mis.jiedaibao.com/) 流程是为 hybird 打造的，编译任务是很吃系统资源的，前端更是如此，在做一些压缩任务的时候，几乎会耗尽内存。当 [mis](http://mis.jiedaibao.com/) 发布频繁时候，机器压力可想而知。

> 针对 mis 的两个问题，已经提出一套编译方案 [jenkins + docker](http://wiki.jdb-dev.com/pages/viewpage.action?pageId=68889060)，并且 mis 已经接入

## 关于 JDBuild

[JDBuild](http://wiki.jdb-dev.com/pages/viewpage.action?pageId=49190604) 是一个简单的编译服务，主要是 OP 上线脚本，他利用了 docker 来保证环境的纯净，并且使用有 http api 服务来调用，将编译结果打包传到 ftp 服务器，并将地址以 response 方式返回。为了加快 `npm install` 的速度，使用 `npm-proxy-cache` 进行缓存。虽然没有 [mis](http://mis.jiedaibao.com/) 那样的功能多样，但是对于上线来说，已经满足需求了(*支付前端在用*)，但还是存在以下问题：

- 扩展问题
- 耗时问题

### 扩展问题

[JDBuild](http://wiki.jdb-dev.com/pages/viewpage.action?pageId=49190604) 服务目前没有在 FE 平台，而是由基础平台部提供，是 docker 集群的一个节点。docker 环境的选择是通过环境变量的映射来进行判断。如果想扩展或修改，要联系相关人员，手动修改 docker 镜像。比如有一段时间，我们想让 JDBuild 来负责 mis 的编译服务，由于 mis 的环境复杂和唯一，做了一个 `mis 1.0.0` 的 docker image，但是回复说可以修改，不能添加，原因可能是能力、人力等。。。

### 耗时问题

[JDBuild](http://wiki.jdb-dev.com/pages/viewpage.action?pageId=49190604) 的启动是通过 HTTP 请求发起的，编译结果当然也是在 response 里返回。部分编译任务非常耗时(*比如APP的打包*)，一次 HTTP 请求是有时间限制的，这里也不好指出具体多少，具体可参考此文章 [maximum reasonable timeout for a synchronous HTTP request](https://stackoverflow.com/questions/33712208/maximum-reasonable-timeout-for-a-synchronous-http-request)


## 总结

根据两个平台的优缺点，考虑受用人群，是可以整合为一套更符合开发流程的编译服务。 [了解更多](introduce.md)
