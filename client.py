import os
import time
import json
from typing import Any, Dict

import requests


# ================== 基础配置 ==================

# 可以用环境变量覆盖：
#   export BASE_URL="https://your-api.com/api/route"
#   export USER_ID="your_user_id"
BASE_URL = os.getenv("BASE_URL", "https://example.com/api/route").rstrip("/")
USER_ID = os.getenv("USER_ID", "").strip()


class ApiError(Exception):
    """自定义异常：用于表示接口调用失败。"""
    pass


def _print_json(prefix: str, data: Any) -> None:
    """
    美化打印 JSON 数据，方便调试。
    """
    try:
        print(prefix, json.dumps(data, ensure_ascii=False, indent=2))
    except TypeError:
        print(prefix, data)


# ================== Step 1: 开始任务 ==================

def start_task(user_id: str) -> str:
    """
    向服务端发起“开始任务”请求，返回 taskId。

    假设服务端返回格式类似：
    {
      "status": "success",
      "data": {
        "taskId": "xxxxxx"
      }
    }
    """
    url = f"{BASE_URL}/startTask"
    data = {
        "userId": user_id
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print(f"[start] POST {url}")
    resp = requests.post(url, data=data, headers=headers, timeout=10)
    print("[start] HTTP 状态码:", resp.status_code)
    print("[start] 原始返回:", resp.text)

    # 如果 HTTP 本身失败（4xx/5xx），这里会抛异常
    resp.raise_for_status()

    try:
        resp_json = resp.json()
    except ValueError as e:
        raise ApiError(f"[start] 返回内容不是合法 JSON: {e}") from e

    _print_json("[start] 解析后的 JSON:", resp_json)

    # 这里根据你实际的接口结构调整
    try:
        task_id = resp_json["data"]["taskId"]
    except (KeyError, TypeError) as e:
        raise ApiError("[start] 无法从返回中解析出 data.taskId") from e

    print("[start] 解析到 taskId:", task_id)
    return task_id


# ================== Step 2: 上报任务进度 ==================

def save_task_progress(user_id: str, task_id: str) -> None:
    """
    上报一次任务进度。

    这里演示一个简单的 payload，你可以按自己的业务需要修改：
    - progress: 当前进度（0~100）
    - elapsedSeconds: 已用时长（秒）
    - timestamp: 当前时间戳（毫秒）
    """
    url = f"{BASE_URL}/saveTaskProgress"

    now_ms = int(time.time() * 1000)

    payload: Dict[str, Any] = {
        "userId": user_id,
        "taskId": task_id,
        "progress": 50,             # 示例：当前进度 50%
        "elapsedSeconds": 600,      # 示例：已用时 600 秒（10 分钟）
        "timestamp": now_ms
    }

    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    print(f"[save] POST {url}")
    _print_json("[save] 请求 JSON:", payload)

    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    print("[save] HTTP 状态码:", resp.status_code)
    print("[save] 返回内容:", resp.text)

    try:
        resp_json = resp.json()
        _print_json("[save] 解析后的 JSON:", resp_json)
    except ValueError:
        # 有些接口可能没有 JSON 返回，这里就不强制报错
        print("[save] 返回的不是 JSON，跳过解析。")


# ================== Step 3: 完成任务 ==================

def finish_task(user_id: str, task_id: str) -> None:
    """
    通知服务端任务已经完成，提交最终结果。

    这里同样只是一个示例 payload：
    - finalProgress: 一般为 100
    - totalSeconds: 任务总耗时
    """
    url = f"{BASE_URL}/finishTask"

    payload: Dict[str, Any] = {
        "userId": user_id,
        "taskId": task_id,
        "finalProgress": 100,
        "totalSeconds": 900,  # 示例：共 900 秒（15 分钟）
        "meta": {
            "comment": "finished from demo client"
        }
    }

    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    print(f"[finish] POST {url}")
    _print_json("[finish] 请求 JSON:", payload)

    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    print("[finish] HTTP 状态码:", resp.status_code)

    try:
        resp_json = resp.json()
        _print_json("[finish] 响应 JSON:", resp_json)
    except ValueError:
        print("[finish] 返回的不是 JSON，原始文本为：")
        print(resp.text)


# ================== Step 4: 查询任务状态 ==================

def get_task_status(user_id: str) -> None:
    """
    查询当前用户的任务状态。

    假设接口返回：
    {
      "status": "success",
      "data": {
        "latestTask": {
          "taskId": "...",
          "status": "done",
          "resultMsg": "xxx"
        }
      }
    }
    """
    url = f"{BASE_URL}/getTaskStatus"

    data = {
        "userId": user_id
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print(f"[status] POST {url}")
    resp = requests.post(url, data=data, headers=headers, timeout=10)
    print("[status] HTTP 状态码:", resp.status_code)
    print("[status] 响应原始内容:", resp.text)

    try:
        j = resp.json()
    except ValueError as e:
        print("[status] 解析 JSON 失败:", e)
        return

    _print_json("[status] 解析后的 JSON:", j)

    # 示例：尝试取出一点关键字段打印
    latest = (j.get("data") or {}).get("latestTask") or {}
    status = latest.get("status")
    result_msg = latest.get("resultMsg")

    print("[status] latestTask.status:", status)
    print("[status] latestTask.resultMsg:", result_msg)


# ================== main 流程 ==================

def main() -> None:
    # 1. 获取 user_id（优先用环境变量，没有则命令行输入）
    user_id = USER_ID
    if not user_id:
        user_id = input("请输入 user_id: ").strip()

    if not user_id:
        print("❌ user_id 不能为空，程序退出。")
        return

    print("当前 BASE_URL:", BASE_URL)
    print("当前 user_id:", user_id)

    try:
        # 2. 开始任务，获得 task_id
        task_id = start_task(user_id)

        # 3. 上报一次任务进度（需要的话可以在这里循环多次调用）
        save_task_progress(user_id, task_id)

        # 4. 完成任务
        finish_task(user_id, task_id)

        # 5. 查询任务状态
        get_task_status(user_id)

    except requests.RequestException as e:
        print("❌ 网络请求异常:", e)
    except ApiError as e:
        print("❌ 接口调用逻辑错误:", e)


if __name__ == "__main__":
    main()
