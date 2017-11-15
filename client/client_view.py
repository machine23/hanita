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
    def render_contacts(self, user_list):
        """ Отображение списка контактов """
        pass

    @abc.abstractmethod
    def render_message(self, message):
        """ Отображение сообщения """
        pass


###############################################################################
# ### ConsoleClientView
###############################################################################
class ConsoleClientView(BaseClientView):
    """ Класс для консольного отображения """
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
    def render_contacts(user_list: list):
        """ Отображение списка контактов """
        if isinstance(user_list, list):
            print("Контакты онлайн:")
            print("\t", ", ".join(user_list), end="\n\n")
        else:
            raise ClientViewError("неверный формат для user_list")

    @staticmethod
    def render_message(message: JIMMessage):
        """ Отображение сообщения """
        if message.action == JIMMessage.MSG:
            print("{}: {}".format(message.from_user, message.message))
