import argparse
import os

class CMD:
    def __init__(self) -> None:
        try:
            arg = argparse.ArgumentParser()
            general_args = arg.add_argument_group(title='Configuration', description='General options')
            general_args.add_argument('-ip',
                                    type=str,
                                    required=True,
                                    help="Set server IP")
            
            general_args.add_argument('-port',
                                    type=int,
                                    required=True,
                                    help="Set server port")
            
            general_args.add_argument('-whitelist',
                                    type=str,
                                    default='',
                                    required=False,
                                    help="Set file with whitelisted IPs")
            
            self.args = arg.parse_args()
        except SystemExit:
            print('Command not recognized!')
            os._exit(8)