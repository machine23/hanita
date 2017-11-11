# import socket

# import pytest

# import actions
# from server import Server, ServerError


# class MySocket:
#     """ заглушка для socket.socket """

#     def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
#         self.data = b""
#         self.addr = None

#     def accept(self):
#         return MySocket(), ("127.0.0.1", 8888)

#     def bind(self, address):
#         pass

#     def listen(self, backlog=None):
#         pass

#     def settimeout(self, timeout):
#         pass

#     def sendall(self, data):
#         self.data = data

#     def recv(self, buffersize):
#         return b'{"action": "presence"}'

#     def close(self):
#         self.data = b""
#         self.addr = None


# @pytest.fixture
# def my_socket():
#     orig_socket = socket.socket
#     socket.socket = MySocket
#     yield
#     socket.socket = orig_socket


# @pytest.fixture
# def server(my_socket):
#     s = Server("127.0.0.1", 8888)
#     yield s
#     s.close()


# def test_parse_msg(server):
#     expected = {"action": "test", "time": 1}
#     bmsg = b'{"action":"test","time":1}'
#     assert server.parse_msg(bmsg) == expected


# def test_create_response_ok(server):
#     expected = {"response": 200, "alert": "ok"}
#     msg = {"action": actions.PRESENCE, "time": 1}
#     assert server.create_response(msg) == expected


# def test_create_response_wrong_msg(server):
#     expected = {"response": 400, "error": "неправильный запрос/JSON-объект"}
#     msg = {"action": "wrong action"}
#     assert server.create_response(msg) == expected


# def test_create_response_wrong_json(server):
#     expected = {"response": 400, "error": "неправильный запрос/JSON-объект"}
#     msg = "this is not json"
#     assert server.create_response(msg) == expected


# def test_clients_close(server):
#     server.clients_close()
#     assert server.clients == []


# def test_close(server):
#     server.close()
#     assert server.sock is None


# ### Тесты, которые нужно заполнить в будущем ###
# def test_accept(server, monkeypatch):
#     # monkeypatch.setattr(server.sock, "accept", lambda: (MySocket(), ("", 8888)))
#     # s = Server("", 8888)
#     expected = [MySocket()]
#     server.accept()
#     assert len(expected) == len(server.clients)
#     assert [type(i) for i in expected] == [type(i) for i in server.clients]

#     def accept_with_error():
#         raise InterruptedError
#     monkeypatch.setattr(server.sock, "accept", accept_with_error)
#     server.accept()
#     assert len(expected) == len(server.clients)


# def test_get(server, monkeypatch):
#     with pytest.raises(ServerError):
#         server.get(MySocket())
#     server.accept()
#     expected = {"action": "presence"}
#     client = server.clients[0]
#     assert expected == server.get(client)

#     def recv_error(buf=None):
#         raise socket.error
#     monkeypatch.setattr(client, "recv", recv_error)
#     server.get(client)
#     assert len(server.clients) == 0


# def test_send(server, monkeypatch):
#     server.accept()
#     client = server.clients[0]
#     with pytest.raises(ServerError):
#         server.send(MySocket, "")
#     with pytest.raises(ServerError):
#         server.send(client, "")
#     server.send(client, {"a": "b"})
#     assert b'{"a": "b"}' == server.clients[0].data

#     def sendall_error(msg):
#         raise socket.error
#     monkeypatch.setattr(client, "sendall", sendall_error)
#     len_before_error = len(server.clients)
#     server.send(client, {"a": "b"})
#     assert len_before_error - len(server.clients) == 1


# def test_send_from_to_all(server):
#     server.accept()
#     server.accept()
#     print(server.clients)
#     to_ = server.clients
#     from_ = server.clients[0]
#     server.send_from_to_all(from_, to_, {"a": "b"})
#     assert server.clients[1].data == b'{"a": "b"}'
