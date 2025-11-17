# Python HTTP Multi-step Client Demo

一个用 Python 编写的 **多步骤 HTTP 接口调用示例**，演示如何：

- 用 `requests` 调用 RESTful 风格接口
- 封装统一的 `BASE_URL` 和公共参数
- 把「开始任务 → 上报进度 → 完成任务 → 查询结果」做成清晰的函数调用流程

> ⚠️ 本项目仅作为 **学习 HTTP 请求与接口封装的示例代码**。  
> 请不要用于绕过任何网站 / 学校 / 平台的正常使用规则，否则产生的后果自行承担。

---

功能概览

整个流程包含 4 个步骤，对应 4 个接口：

1. `start_task(user_id)`  
   - 向服务端发起“开始任务”请求  
   - 返回一个 `taskId`

2. `save_task_progress(user_id, task_id)`  
   - 模拟上报一次任务进度，例如：当前进度、用时等

3. `finish_task(user_id, task_id)`  
   - 通知服务端“任务已完成”，提交最终结果（总时长、总进度等）

4. `get_task_status(user_id)`  
   - 查询当前用户最近一次任务的状态

你可以根据自己的服务端实现来调整这些字段和逻辑。

---
环境准备
`git clone https://github.com/98364/python-http-multi-step-client-demo.git`
`cd python-http-multi-step-client-demo`
安装依赖
`pip install -r requirements.txt`

使用方法
1.在 client.py 中设置你的 BASE_URL 和 USER_ID：

`BASE_URL = "https://example.com/api"  # 改成你自己的接口地址`

`USER_ID = "your_user_id_here"`

2.运行脚本

`python client.py`

你会在终端看到类似这样的输出（示例）：

`[start] HTTP 状态码: 200`

`[start] 原始返回: {"status": "success", "data": {"taskId": "xxxx"}}`

`[start] 解析到 taskId: xxxx`

`[save] HTTP 状态码: 200`

`[save] 返回内容: {...}`

`[finish] HTTP 状态码: 200`

`[finish] 响应 JSON: { ... }`

`[select] HTTP 状态码: 200`

`[select] 响应原始内容: {...}`


注意事项 & 免责声明

本项目只演示「如何写 HTTP 客户端代码」，不附带任何真实线上服务。

请遵守你所访问系统的《用户协议》《服务条款》以及你所在学校 / 公司的相关规定。

⚠️请不要用于：

- 伪造考勤 / 打卡记录

- 绕过课程、考试、体测等强制性要求

未经授权的大规模自动化访问

⚠️ 一切因为不当使用本示例代码造成的后果，由使用者自行承担。



