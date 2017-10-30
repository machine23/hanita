import argparse
import json
import socket


def run_server(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen()

    try:
        while True:
            client, addr = sock.accept()
            msg = get_message(client)
            resp = create_response(msg)
            send_response(client, resp)
            client.close()
    except KeyboardInterrupt:
        pass
    
    sock.close()


def get_message(client):
    return {}


def create_response(msg):
    pass


def send_response(client, response):
    pass


####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", default="bla", nargs="?", help="HOST")
    parser.add_argument("-a", dest="addr", help="IP-адрес для прослушивания")
    parser.add_argument("-p", dest="port", type=int, 
                        help="TCP-порт (по умолчанию 7777)")

    args = parser.parse_args()
    print("host:", args.host, type(args.host))
    print("addr:", args.addr, type(args.addr))
    print("port:", args.port, type(args.port))