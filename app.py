from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from cmd_args import CMD

import os
import sys
import uvicorn
import subprocess

PLATFORM = sys.platform.upper()
cmd = CMD().args
app = FastAPI()
server_ip = cmd.ip
server_port = cmd.port
whitelist = cmd.whitelist

def parse_whitelist_file():
    with open('whitelist.txt', 'r') as f:
        return f.read().splitlines()

def is_whitelisted(client_ip: str, allowed_ips: list):
    if client_ip not in allowed_ips:
        return False
    return True

@app.get('/', response_class=JSONResponse)
async def index(request: Request, path: str, cmd: str):
    client_ip = request.client.host
    if whitelist != '':
        allowed_ips = parse_whitelist_file()
        if is_whitelisted(client_ip, allowed_ips) != True:
            return {'error': True, 'message': 'failed to connect'}
    
    command = f'cd {path}; {cmd}' if PLATFORM == 'LINUX' else f'cd {path} && {cmd}'
    # print(f'Client IP: {client_ip}')
    # print(f'Path: {path}')
    # print(f'Cmd: {cmd}')
    # print(command)
    
    try:
        # os.system(command)
        # return {'error': False, 'message': 'ok'}
        output = subprocess.check_output(command, shell=True, start_new_session=True)
        return {'error': False, 'message': output}
    except Exception as err:
        return {'error': True, 'message': 'failed to execute command', 'reason': err}


if __name__ == "__main__":
    uvicorn.run("app:app", host=server_ip, port=server_port, log_level="info")