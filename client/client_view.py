""" классы для UI клиентского приложения """
import abc
import os

from JIM import JIMMessage


###############################################################################
# ### ClientViewError
###############################################################################
class ClientViewError(Exception):
    """ Базовое исключение для классов *ClientView """
    pass


###############################################################################
# ### BaseClientView
###############################################################################
class BaseClientView(metaclass=abc.ABCMeta):
    """ Базовый абстрактный класс для *ClientView классов """
    @abc.abstractmethod
    def greet(self, user_name):
        """ Отображение приветствия и первоночальная подсказка """
        pass

    @abc.abstractmethod
    def render_contacts(self, user_list, info):
        """ Отображение списка контактов """
        pass

    @abc.abstractmethod
    def render_message(self, message):
        """ Отображение сообщения """
        pass

    @abc.abstractmethod
    def render_info(self, info):
        """ Информационное сообщение """
        pass

    @abc.abstractmethod
    def input(self, msg):
        """ Получить ввод от пользователя """
        pass

    @abc.abstractmethod
    def render_help(self):
        """ Показать подсказку """
        pass

    @abc.abstractmethod
    def model_is_changed(self):
        """ Действия при изменении модели """
        pass


###############################################################################
# ### ConsoleClientView
###############################################################################
class ConsoleClientView(BaseClientView):
    """ Класс для консольного отображения """
    def __init__(self, client=None, model=None):
        pass

    @staticmethod
    def _clear():
        """ Очистить консоль """
        os.system("cls" if os.name == "nt" else "clear")

    def greet(self, user_name=""):
        """ Отображение приветствия и первоночальная подсказка """
        if not user_name:
            user_name = "Гость"
        self._clear()
        print("\tПривет,", user_name)

    @staticmethod
    def render_contacts(user_list: list, info=""):
        """ Отображение списка контактов """
        if isinstance(user_list, list):
            if info:
                print(info, end=" ")
            print("\t", ", ".join(user_list), end="\n\n")
        else:
            raise ClientViewError("неверный формат для user_list")

    @staticmethod
    def render_message(message: JIMMessage):
        """ Отображение сообщения """
        if message.action == JIMMessage.MSG:
            print("{}: {}".format(message.from_user, message.message))

    @staticmethod
    def render_info(info):
        """ отображение информационного сообщения """
        print("\n", info)

    @staticmethod
    def input(msg):
        return input(msg)

    @staticmethod
    def render_help():
        help_str = """
                                Hanita
        ====================================================================
        Справка по консольным командам.
        >>> @                   - узнать, кто онлайн;
        >>> @nickname [message] - отправить сообщение пользователю nickname;
        >>> !contacts           - получить список контактов;
        >>> !add nickname       - добавить nickname в контакты;
        >>> !del nickname       - удалить nickname из контактов (в разработке);
        >>> !quit               - выйти из программы;
        >>> !help               - вывести эту справку.

        """
        print(help_str)

    def model_is_changed(self):
        pass

    def run(self):
        pass