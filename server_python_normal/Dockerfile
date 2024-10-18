FROM python:3.9-slim

RUN pip3 install websockets

# RUN pip3 install requests

COPY ./python_server.py home/root/WEB_SOCKET_WS/server_normal_python/python_server.py
RUN chmod +x /home/root/WEB_SOCKET_WS/server_normal_python/python_server.py

WORKDIR /home/root/WEB_SOCKET_WS/server_normal_python/
CMD ["python3", "python_server.py"]
