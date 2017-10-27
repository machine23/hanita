import argparse
import socket
import time


class Client:
    def __init__(self, user, status=""):
        self.user = user
        self.status = status
    
    