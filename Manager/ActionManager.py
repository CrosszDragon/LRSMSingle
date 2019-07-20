# -*- coding: utf-8 -*-
# @Time    : 2019/7/2 16:00
# @Author  : 何盛信
# @Email   : 2958029539@qq.com
# @File    : ActionManager.py
# @Project : LSRMSingleVersion3
# @Software: PyCharm

from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QKeySequence
from Manager.Id import Id


class ActionManager(QObject):
    """
    单例模式
    Manager of global actions.
    """

    class ActionManagerPrivate:

        def __init__(self):
            self.id_to_action_dict = {}
            self.id_to_menu_dict = {}

            # 默认的 快捷键 用来重置快捷键
            self.default_shortcuts = {}
            self.custom_shortcuts = {}
            # 用来检测 快捷键的改变
            self.last_known_shortcuts = {}

            self.applying_shortcut = False
            self.resetting_shortcut = False

    action_changed = pyqtSignal(Id)
    actions_changed = pyqtSignal()

    _instance = None
    _d = ActionManagerPrivate()

    def __init__(self, parent=None):
        if ActionManager._instance is None:
            QObject.__init__(self, parent)
            # ActionManager.read_custom_shortcuts()
            ActionManager._instance = self
        else:
            raise SyntaxError("ActionManger是单例类，请通过静态函数instance获取其实力")

    @staticmethod
    def instance(parent=None):
        if ActionManager._instance is None:
            ActionManager._instance = ActionManager(parent)
        return ActionManager._instance

    def has_custom_shortcut(self, action_id: Id):
        """TODO"""

    def set_custom_shortcut(self, action_id: Id, key_sequence: QKeySequence):
        """TODO"""

    def reset_custom_shortcut(self, action_id: Id):
        """TODO"""

    def reset_all_custom_shortcuts(self):
        """TODO"""

    def default_shortcut(self, action_id: Id) -> QKeySequence:
        """TODO"""

    @staticmethod
    def register_action(action: QAction, action_id: Id):
        """
        用action_id向action管理器注册action
        :param action: 要注册的action
        :param action_id: 标识该action的id
        """
        # def action_changed():
        #     if not ActionManager._d.applying_shortcut and action_id in ActionManager._d.default_shortcuts and \
        #             ActionManager._d.last_known_shortcuts[action_id] != action.shortcut():
        #         # 更新默认的快捷键
        #         ActionManager._d.default_shortcuts[action_id] = action.shortcut()
        #         # 重置 回自定义的快捷键
        #         if action_id in ActionManager._d.custom_shortcuts:
        #             ActionManager.apply_shortcut(action, ActionManager._d.custom_shortcuts[action_id])
        #             return
        #     try:
        #         ActionManager._d.last_known_shortcuts[action_id] = action.shortcut()
        #         ActionManager.instance().action_changed.emit(action_id)
        #     except Exception as e:
        #         print("action change 警告", e)
        #         QMessageBox.warning(action.parentWidget(), title="action change 警告", text=str(e))

        try:
            assert action_id not in ActionManager._d.id_to_action_dict
            ActionManager._d.id_to_action_dict[action_id] = action
            ActionManager._d.last_known_shortcuts[action_id] = action.shortcut()
            # action.changed.connect(action_changed)

            if ActionManager.instance().has_custom_shortcut(action_id):
                ActionManager._d.default_shortcuts[action_id] = action.shortcut()
                ActionManager.apply_shortcut(action, ActionManager._d.custom_shortcuts[action_id])
            ActionManager.instance().actions_changed.emit()
        except AssertionError as e:
            """"""
            print("ActionManager action id = {0} 重复" .format(action_id))

    @staticmethod
    def unregister_action(action_id: Id):
        try:
            assert action_id in ActionManager._d.id_to_action_dict
            action = ActionManager._d.id_to_action_dict[action_id]
            action.disconnect(ActionManager())
            del ActionManager._d.id_to_action_dict[action_id]
            if action_id in ActionManager._d.default_shortcuts:
                del ActionManager._d.default_shortcuts[action_id]
            if action_id in ActionManager._d.last_known_shortcuts:
                del ActionManager._d.last_known_shortcuts[action_id]
            ActionManager.instance().actions_changed.emit()
        except AssertionError as e:
            print("action unregister 警告: ", e)
            # QMessageBox.warning(action.parentWidget(), title="action unregister 警告", text=str(e))

    @staticmethod
    def register_menu(menu: QMenu, menu_id: Id):
        if menu_id in ActionManager._d.id_to_menu_dict:
            ActionManager._d.id_to_menu_dict[menu_id] = menu

    @staticmethod
    def unregister_menu(menu_id: Id):
        if menu_id in ActionManager._d.id_to_menu_dict:
            del ActionManager._d.id_to_menu_dict[menu_id]

    @staticmethod
    def action(action_id: Id) -> QAction:
        try:
            return ActionManager._d.id_to_action_dict[action_id]
        except KeyError:
            print("id to action error: ", action_id)
            return QAction()

    @staticmethod
    def find_action(action_id: Id) -> QAction:
        return ActionManager.action(action_id)

    @staticmethod
    def menu(menu_id: Id) -> QMenu:
        try:
            return ActionManager._d.id_to_menu_dict[menu_id]
        except KeyError:
            return None

    @staticmethod
    def find_menu(menu_id: Id) -> QAction:
        return ActionManager.action(menu_id)

    @staticmethod
    def actions() -> tuple:
        return tuple(ActionManager._d.id_to_action_dict.keys())

    @staticmethod
    def menus() -> tuple:
        return tuple(ActionManager._d.id_to_menu_dict.keys())

    @staticmethod
    def read_custom_shortcuts():
        """TODO"""

    @staticmethod
    def apply_shortcut(action: QAction, shortcut: QKeySequence):
        ActionManager._d.applying_shortcut = True
        action.setShortcut(shortcut)
        ActionManager._d.applying_shortcut = False


# ActionManagerInstance = Singleton(ActionManager)


if __name__ == '__main__':
    action_manager1 = ActionManager.instance()

    action_manager2 = ActionManager.instance()

    print(action_manager1 == action_manager2)
    print(id(action_manager1) == id(action_manager2))

    action_manager1.m = "action manager1 instance"

    print(action_manager1)
    del action_manager1
    print(action_manager2)
