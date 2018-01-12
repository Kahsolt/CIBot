# CIBot
    
    A hybrid chatbot-like QA platform enhanced by crowd intelligence...

---

- **Architecture Briefs**
  - 前端
    - 自制Web页面
      - jQuery Ajax轮询
      - Django的websocket集成考虑用[Channels](http://channels.readthedocs.io/en/stable)
    - 依赖在线聊天平台，以及基于该平台的SDK/命令行客户端/机器人作适配器
      - Wechat + [wxBot](https://github.com/liuwons/wxBot)
      - Discord + [discord.py](https://github.com/Rapptz/discord.py)
  - 后端
    - 本Django工程本身作为数据库管理+信息处理中枢
    - 问答AI接口(推荐有)
      - [QA-Snake](https://github.com/SnakeHacker/QA-Snake)
      - [图灵机器人](http://www.tuling123.com/)

- **Run**
  - sh ./bin/db migrate(首次运行)
  - sh ./bin/cibot start

- **Dev**
  - 环境依赖参考DEPENDENCIES
  - 工程文件概貌参考STRUCTURE
  - 开发文档参考doc目录
  - 上传务必注意.gitignore

- **Port Info**
  - 8000    Django
  - 50000   QA-Snake

