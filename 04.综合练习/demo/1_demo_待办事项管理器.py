# ============================================================
# Demo 1: 命令行待办事项管理器
# 综合练习 —— 整合前三章所有知识点
# ============================================================
# 这个 Demo 实现了一个完整的命令行待办事项管理器。
# 代码中用注释标注每个部分用到了前面哪一章的什么知识点。
# 不需要 API Key。
# ============================================================

import json
import os
from datetime import datetime


# ============================================================
# 【第2章·类与对象】定义 TodoItem 类
# ============================================================
# 用类来表示一个待办事项，包含标题、描述、状态等属性。
# 这是面向对象编程的核心：把数据和操作打包在一起。
# ============================================================

class TodoItem:
    """
    单个待办事项类

    【知识点】
    - class: 定义类
    - __init__: 构造方法，创建对象时自动调用
    - self: 代表当前对象自身
    - self.xxx: 实例属性
    - @classmethod: 类方法，用另一种方式创建对象
    - __str__: 魔术方法，定义 print() 时的输出
    """

    # 【第2章·类与对象】类属性：所有对象共享
    _counter = 0    # 用于生成唯一 ID

    def __init__(self, title, description="", priority="中"):
        """
        【第2章·类与对象】构造方法
        创建 TodoItem 对象时自动调用
        """
        TodoItem._counter += 1
        self.id = TodoItem._counter              # 唯一 ID
        self.title = title                        # 标题
        self.description = description            # 描述
        self.priority = priority                  # 优先级：高/中/低
        self.completed = False                    # 是否完成
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")  # 创建时间
        self.completed_at = None                  # 完成时间

    def mark_completed(self):
        """
        【第1章·函数】方法：标记为已完成
        """
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_uncompleted(self):
        """标记为未完成"""
        self.completed = False
        self.completed_at = None

    def to_dict(self):
        """
        【第2章·文件操作】将对象转为字典，用于保存到 JSON
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        """
        【第2章·类与对象】类方法：从字典创建对象
        用于从 JSON 文件加载数据
        """
        item = cls(data["title"], data.get("description", ""), data.get("priority", "中"))
        item.id = data.get("id", 0)
        item.completed = data.get("completed", False)
        item.created_at = data.get("created_at", "")
        item.completed_at = data.get("completed_at")
        # 更新计数器，确保新创建的 ID 不会重复
        if item.id >= TodoItem._counter:
            TodoItem._counter = item.id
        return item

    def __str__(self):
        """
        【第2章·类与对象】魔术方法：定义 print(todo) 时的输出
        """
        status = "✅" if self.completed else "⬜"
        priority_map = {"高": "🔴", "中": "🟡", "低": "🟢"}
        priority_icon = priority_map.get(self.priority, "⚪")
        return f"  {status} [{self.id:03d}] {priority_icon} {self.title}"

    def detail(self):
        """返回详细信息"""
        status = "已完成" if self.completed else "未完成"
        lines = [
            f"  ID: {self.id}",
            f"  标题: {self.title}",
            f"  描述: {self.description or '无'}",
            f"  优先级: {self.priority}",
            f"  状态: {status}",
            f"  创建时间: {self.created_at}",
        ]
        if self.completed_at:
            lines.append(f"  完成时间: {self.completed_at}")
        return "\n".join(lines)


# ============================================================
# 【第2章·类与对象】定义 TodoManager 类
# ============================================================
# 用组合的方式，让 TodoManager 管理多个 TodoItem。
# 这体现了"单一职责原则"：TodoItem 管数据，TodoManager 管逻辑。
# ============================================================

class TodoManager:
    """
    待办事项管理器

    【知识点】
    - 类的组合：TodoManager 内部包含多个 TodoItem
    - 列表操作：增删改查
    - 文件操作：JSON 读写
    - 异常处理：文件不存在时优雅处理
    """

    def __init__(self, filepath="todos.json"):
        """
        【第2章·类与对象】构造方法
        - filepath: 数据文件路径
        """
        self.filepath = filepath
        self.todos = []    # 【第1章·数据类型】列表，存储所有待办事项
        self.load()        # 启动时自动加载数据

    # ----- 增删改查（CRUD） -----

    def add(self, title, description="", priority="中"):
        """
        【第1章·函数】添加待办事项
        """
        # 【第2章·异常处理】输入验证
        if not title.strip():
            raise ValueError("标题不能为空")

        if priority not in ("高", "中", "低"):
            raise ValueError(f"优先级必须是 高/中/低，收到: {priority}")

        todo = TodoItem(title.strip(), description.strip(), priority)
        self.todos.append(todo)
        self.save()    # 【第2章·文件操作】每次修改后自动保存
        return todo

    def get_all(self):
        """获取所有待办事项"""
        return self.todos

    def get_by_id(self, todo_id):
        """
        根据 ID 获取待办事项
        【第1章·条件判断与循环】遍历查找
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def get_pending(self):
        """获取未完成的待办事项"""
        # 【第1章·数据类型】列表推导式
        return [t for t in self.todos if not t.completed]

    def get_completed(self):
        """获取已完成的待办事项"""
        return [t for t in self.todos if t.completed]

    def complete(self, todo_id):
        """
        标记待办事项为已完成
        """
        todo = self.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"ID {todo_id} 不存在")
        if todo.completed:
            raise ValueError(f"ID {todo_id} 已经是完成状态")
        todo.mark_completed()
        self.save()
        return todo

    def uncomplete(self, todo_id):
        """标记待办事项为未完成"""
        todo = self.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"ID {todo_id} 不存在")
        todo.mark_uncompleted()
        self.save()
        return todo

    def delete(self, todo_id):
        """
        删除待办事项
        【第1章·条件判断与循环】列表过滤
        """
        todo = self.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"ID {todo_id} 不存在")
        self.todos = [t for t in self.todos if t.id != todo_id]
        self.save()
        return todo

    def edit(self, todo_id, title=None, description=None, priority=None):
        """编辑待办事项"""
        todo = self.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"ID {todo_id} 不存在")
        if title is not None:
            todo.title = title.strip()
        if description is not None:
            todo.description = description.strip()
        if priority is not None:
            if priority not in ("高", "中", "低"):
                raise ValueError(f"优先级必须是 高/中/低")
            todo.priority = priority
        self.save()
        return todo

    def search(self, keyword):
        """
        搜索待办事项
        【第1章·条件判断与循环】字符串匹配
        """
        keyword = keyword.lower()
        return [t for t in self.todos
                if keyword in t.title.lower() or keyword in t.description.lower()]

    def get_stats(self):
        """
        获取统计信息
        【第1章·数据类型】字典
        """
        total = len(self.todos)
        completed = len(self.get_completed())
        pending = total - completed
        return {
            "总数": total,
            "已完成": completed,
            "未完成": pending,
            "完成率": f"{completed/total*100:.1f}%" if total > 0 else "N/A"
        }

    # ----- 持久化存储 -----

    def save(self):
        """
        【第2章·文件操作】保存到 JSON 文件
        把所有 TodoItem 对象转为字典列表，写入 JSON 文件
        """
        data = [todo.to_dict() for todo in self.todos]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        """
        【第2章·文件操作 + 异常处理】从 JSON 文件加载
        文件不存在时创建空列表，不会报错
        """
        try:
            # 【第2章·异常处理】捕获文件不存在的异常
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 【第2章·类与对象】从字典创建对象（类方法）
            self.todos = [TodoItem.from_dict(d) for d in data]
            # 更新计数器
            if self.todos:
                TodoItem._counter = max(t.id for t in self.todos)
        except FileNotFoundError:
            # 【第2章·异常处理】文件不存在时使用空列表
            self.todos = []
        except json.JSONDecodeError:
            # 【第2章·异常处理】JSON 格式错误时使用空列表
            print(f"⚠ 警告: {self.filepath} 格式错误，将使用空数据")
            self.todos = []


# ============================================================
# 【第1章·函数】定义用户界面函数
# ============================================================
# 把 UI 相关的函数和业务逻辑分开，职责清晰。
# ============================================================

def print_separator(char="=", length=50):
    """【第1章·函数】打印分隔线"""
    print(char * length)


def print_header(title):
    """【第1章·函数】打印标题"""
    print()
    print_separator()
    print(f"  {title}")
    print_separator()


def show_main_menu():
    """
    【第1章·函数 + 字符串】显示主菜单
    """
    print()
    print_separator("-")
    print("  📋 待办事项管理器")
    print_separator("-")
    print("  1. 查看所有待办")
    print("  2. 查看未完成待办")
    print("  3. 查看已完成待办")
    print("  4. 添加待办事项")
    print("  5. 标记完成")
    print("  6. 标记未完成")
    print("  7. 编辑待办事项")
    print("  8. 删除待办事项")
    print("  9. 搜索待办事项")
    print("  10. 查看统计")
    print("  0. 退出")
    print_separator("-")


def show_todo_list(todos, title="待办事项列表"):
    """
    【第1章·条件判断与循环】显示待办事项列表
    """
    print_header(title)
    if not todos:
        print("  (空)")
        return
    for todo in todos:
        print(todo)


def get_input(prompt, validator=None, error_msg="输入无效，请重试"):
    """
    【第2章·异常处理】安全地获取用户输入
    - prompt: 提示信息
    - validator: 验证函数（返回 True/False）
    - error_msg: 验证失败时的提示
    """
    while True:
        try:
            value = input(prompt).strip()
            if validator and not validator(value):
                print(f"  ⚠ {error_msg}")
                continue
            return value
        except (EOFError, KeyboardInterrupt):
            print("\n  已取消")
            return None


def get_int_input(prompt):
    """
    【第2章·异常处理】安全地获取整数输入
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                return None
            return int(value)
        except ValueError:
            print("  ⚠ 请输入数字")


# ============================================================
# 【第1章·函数】定义各个操作的处理函数
# ============================================================

def handle_add(manager):
    """处理添加待办事项"""
    print_header("添加待办事项")

    title = get_input("  请输入标题: ")
    if not title:
        return

    description = input("  请输入描述（可选，直接回车跳过）: ").strip()

    priority = get_input(
        "  请输入优先级（高/中/低，默认中）: ",
        validator=lambda x: x in ("高", "中", "低", ""),
        error_msg="优先级必须是 高/中/低"
    )
    if not priority:
        priority = "中"

    try:
        # 【第2章·异常处理】捕获业务逻辑错误
        todo = manager.add(title, description, priority)
        print(f"\n  ✅ 添加成功: {todo}")
    except ValueError as e:
        print(f"\n  ❌ 添加失败: {e}")


def handle_complete(manager):
    """处理标记完成"""
    show_todo_list(manager.get_pending(), "未完成的待办事项")

    todo_id = get_int_input("\n  请输入要标记完成的 ID: ")
    if todo_id is None:
        return

    try:
        todo = manager.complete(todo_id)
        print(f"\n  ✅ 已完成: {todo}")
    except ValueError as e:
        print(f"\n  ❌ 操作失败: {e}")


def handle_uncomplete(manager):
    """处理标记未完成"""
    show_todo_list(manager.get_completed(), "已完成的待办事项")

    todo_id = get_int_input("\n  请输入要标记未完成的 ID: ")
    if todo_id is None:
        return

    try:
        todo = manager.uncomplete(todo_id)
        print(f"\n  ✅ 已标记为未完成: {todo}")
    except ValueError as e:
        print(f"\n  ❌ 操作失败: {e}")


def handle_edit(manager):
    """处理编辑待办事项"""
    show_todo_list(manager.get_all(), "所有待办事项")

    todo_id = get_int_input("\n  请输入要编辑的 ID: ")
    if todo_id is None:
        return

    todo = manager.get_by_id(todo_id)
    if todo is None:
        print(f"\n  ❌ ID {todo_id} 不存在")
        return

    print(f"\n  当前信息:")
    print(todo.detail())

    print(f"\n  直接回车表示不修改")
    new_title = input(f"  新标题 [{todo.title}]: ").strip()
    new_desc = input(f"  新描述 [{todo.description}]: ").strip()
    new_priority = input(f"  新优先级 [{todo.priority}]: ").strip()

    try:
        manager.edit(
            todo_id,
            title=new_title or None,
            description=new_desc if new_desc != "" else None,
            priority=new_priority or None
        )
        print(f"\n  ✅ 编辑成功: {manager.get_by_id(todo_id)}")
    except ValueError as e:
        print(f"\n  ❌ 编辑失败: {e}")


def handle_delete(manager):
    """处理删除待办事项"""
    show_todo_list(manager.get_all(), "所有待办事项")

    todo_id = get_int_input("\n  请输入要删除的 ID: ")
    if todo_id is None:
        return

    todo = manager.get_by_id(todo_id)
    if todo is None:
        print(f"\n  ❌ ID {todo_id} 不存在")
        return

    # 【第1章·条件判断】确认删除
    confirm = input(f"  确认删除 '{todo.title}'？(y/N): ").strip().lower()
    if confirm != "y":
        print("  已取消")
        return

    try:
        manager.delete(todo_id)
        print(f"\n  ✅ 已删除: {todo}")
    except ValueError as e:
        print(f"\n  ❌ 删除失败: {e}")


def handle_search(manager):
    """处理搜索"""
    keyword = get_input("  请输入搜索关键词: ")
    if not keyword:
        return

    results = manager.search(keyword)
    show_todo_list(results, f"搜索结果: '{keyword}'")

    if results:
        print(f"\n  找到 {len(results)} 条结果")


def handle_stats(manager):
    """处理统计"""
    stats = manager.get_stats()
    print_header("统计信息")
    for key, value in stats.items():
        print(f"  {key}: {value}")


# ============================================================
# 【第1章·条件判断与循环 + 第2章·异常处理】主程序
# ============================================================
# 用 while 循环实现菜单的持续交互
# 用 try/except 处理各种可能的错误
# ============================================================

def main():
    """
    主函数：程序入口

    【知识点汇总】
    - 第1章: 变量、条件判断、循环、函数
    - 第2章: 类与对象、文件操作、异常处理
    - 第4章: 项目规划与代码组织
    """
    print("\n" + "=" * 50)
    print("  欢迎使用命令行待办事项管理器！")
    print("  数据将保存在 todos.json 文件中")
    print("=" * 50)

    # 【第2章·类与对象】创建管理器实例
    manager = TodoManager("todos.json")

    # 显示已加载的数据
    stats = manager.get_stats()
    if stats["总数"] > 0:
        print(f"\n  已从文件加载 {stats['总数']} 条待办事项")

    # 【第1章·条件判断与循环】主循环
    while True:
        try:
            show_main_menu()
            choice = input("  请输入选项编号: ").strip()

            # 【第1章·条件判断】根据用户选择执行不同操作
            if choice == "1":
                show_todo_list(manager.get_all(), "所有待办事项")
            elif choice == "2":
                show_todo_list(manager.get_pending(), "未完成的待办事项")
            elif choice == "3":
                show_todo_list(manager.get_completed(), "已完成的待办事项")
            elif choice == "4":
                handle_add(manager)
            elif choice == "5":
                handle_complete(manager)
            elif choice == "6":
                handle_uncomplete(manager)
            elif choice == "7":
                handle_edit(manager)
            elif choice == "8":
                handle_delete(manager)
            elif choice == "9":
                handle_search(manager)
            elif choice == "10":
                handle_stats(manager)
            elif choice == "0":
                print("\n  👋 再见！数据已自动保存。")
                break
            else:
                print("\n  ⚠ 无效选项，请输入 0-10")

        except KeyboardInterrupt:
            # 【第2章·异常处理】处理 Ctrl+C
            print("\n\n  👋 再见！数据已自动保存。")
            break
        except Exception as e:
            # 【第2章·异常处理】兜底处理，防止程序崩溃
            print(f"\n  ❌ 发生未知错误: {e}")
            print("  程序将继续运行...")


# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    main()
