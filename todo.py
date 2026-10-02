#!/usr/bin/env python3
"""命令行待办事项管理器（仅使用 Python 标准库）"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def load_tasks():
    """从 JSON 文件加载任务列表"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        print("警告：数据文件损坏或无法读取，已重置为空列表。")
        return []


def save_tasks(tasks):
    """将任务列表保存到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(tasks):
    """添加任务"""
    title = input("请输入任务内容：").strip()
    if not title:
        print("任务内容不能为空。")
        return
    task = {
        "id": (max((t["id"] for t in tasks), default=0)) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"已添加任务 [{task['id']}]：{title}")


def list_tasks(tasks):
    """查看任务列表"""
    if not tasks:
        print("当前没有任务。")
        return
    print("\n===== 任务列表 =====")
    print(f"{'ID':<4}{'状态':<6}{'任务内容':<30}创建时间")
    print("-" * 56)
    for t in tasks:
        status = "已完成" if t["done"] else "未完成"
        print(f"{t['id']:<4}{status:<6}{t['title']:<30}{t['created_at']}")
    done = sum(1 for t in tasks if t["done"])
    print(f"\n共 {len(tasks)} 项，已完成 {done} 项。")


def complete_task(tasks):
    """标记任务为已完成"""
    if not tasks:
        print("当前没有任务。")
        return
    task_id = ask_task_id()
    if task_id is None:
        return
    task = find_task(tasks, task_id)
    if task is None:
        print(f"未找到 ID 为 {task_id} 的任务。")
        return
    if task["done"]:
        print(f"任务 [{task_id}] 已经是完成状态。")
        return
    task["done"] = True
    save_tasks(tasks)
    print(f"已将任务 [{task_id}] 标记为完成。")


def delete_task(tasks):
    """删除任务"""
    if not tasks:
        print("当前没有任务。")
        return
    task_id = ask_task_id()
    if task_id is None:
        return
    task = find_task(tasks, task_id)
    if task is None:
        print(f"未找到 ID 为 {task_id} 的任务。")
        return
    confirm = input(f"确定删除任务 [{task_id}]「{task['title']}」吗？(y/n)：").strip().lower()
    if confirm != "y":
        print("已取消删除。")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print(f"已删除任务 [{task_id}]。")


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def ask_task_id():
    """读取并校验任务 ID 输入"""
    raw = input("请输入任务 ID：").strip()
    if not raw.isdigit():
        print("请输入有效的数字 ID。")
        return None
    return int(raw)


def main():
    tasks = load_tasks()
    print("欢迎来到待办事项管理器！")
    while True:
        print("\n===== 菜单 =====")
        print("1. 查看任务")
        print("2. 添加任务")
        print("3. 标记完成")
        print("4. 删除任务")
        print("5. 退出")
        choice = input("请选择操作：").strip()
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选项，请重新选择。")


if __name__ == "__main__":
    main()
