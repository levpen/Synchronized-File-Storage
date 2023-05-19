import argparse
import datetime
import json
import os.path

from config import Config, read_config
from api import ApiClient


def parse_date_from(src: str) -> datetime:
    allowed = ['year', 'day', 'hour', 'min', 'sec']
    for a in allowed:
        if src.endswith(a):
            n = int(src.split(a)[0])
            dlt = datetime.timedelta()
            if a == 'year':
                dlt = datetime.timedelta(days=365 * n)
            elif a == 'day':
                dlt = datetime.timedelta(days=n)
            elif a == 'hour':
                dlt = datetime.timedelta(hours=n)
            elif a == 'min':
                dlt = datetime.timedelta(minutes=n)
            elif a == 'sec':
                dlt = datetime.timedelta(seconds=n)
            return datetime.datetime.now() - dlt

    raise Exception(f"{src} does not contain {allowed}")


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='client', description='Synchronized-File-Storage client')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

        subparsers = parser.add_subparsers(title='commands', dest='command')

        # Subparser for the 'sync' command
        sync_parser = subparsers.add_parser('sync', help='Sync data')
        sync_parser.add_argument('-d', '--date', nargs=1, help='Argument for date_from '
                                                               '(format for year,day,hour,min,sec) ', required=True)
        sync_parser.add_argument('-dirs', '--dirs', nargs='+', help='Argument for dirs', required=False)
        sync_parser.set_defaults(func=self.sync)

        # Subparser for the 'info' command
        info_parser = subparsers.add_parser('info', help='List config data')
        info_parser.set_defaults(func=self.info)

        # Subparser for the 'push' command
        push_parser = subparsers.add_parser('push', help='Push data')
        push_parser.add_argument('file_names', nargs='+', help='Arguments for push command')
        push_parser.set_defaults(func=self.push)

        # Subparser for the 'delete' command
        delete_parser = subparsers.add_parser('delete', help='Delete data')
        delete_parser.add_argument('file_names', nargs='+', help='Arguments for delete command')
        delete_parser.set_defaults(func=self.delete)

        # Subparser for the 'setup' command
        setup_parser = subparsers.add_parser('setup', help='Setup client')
        setup_parser.set_defaults(func=self.setup)

        args = parser.parse_args()

        if args.command != 'setup':
            self.config = read_config()
            if self.config is None:
                return
            self.api_client = ApiClient(self.config)

        # Call the appropriate command function based on the subparser selected
        if hasattr(args, 'func'):
            args.func(args)

    def sync(self, args):
        verbose = args.verbose
        date_from: datetime.datetime = datetime.datetime.now()
        dirs = args.dirs
        try:
            date_from = parse_date_from(args.date[0])
        except Exception as err:
            print(f"ERROR\tfailed to parse: {err}")
            return
        result = self.api_client.sync(date_from.timestamp(), dirs=dirs)

        errors = 0
        if not result:
            errors += 1
            self._done(errors)

        overwrite = 0
        created = 0

        data = json.loads(result)
        for file_name in data:
            file_data = data.get(file_name)
            # checking file exits
            try:
                if os.path.isfile(file_name):
                    if verbose:
                        print(f"overwriting '{file_name}'...")
                    with open(file_name, 'w') as f:
                        f.write(file_data)
                        f.close()
                        overwrite += 1
                else:
                    if verbose:
                        print(f"creating '{file_name}'...")
                    with open(file_name, 'a') as f:
                        f.write(file_data)
                        created += 1
            except Exception as e:
                print(f"ERROR\tunknown error: {e}, file={file_name}")

        self._done(errors, overwrite=overwrite, created=created)

    def push(self, args):
        verbose = args.verbose
        errors = 0
        for file_name in args.file_names:
            if self.api_client.push(file_name):
                if verbose:
                    print(f"{file_name} ✔")
            else:
                errors += 1
                if verbose:
                    print(f"{file_name} ✖")
        self._done(errors)

    def delete(self, args):
        verbose = args.verbose
        errors = 0
        for file_name in args.file_names:
            if self.api_client.delete(file_name):
                if verbose:
                    print(f"{file_name} ✔")
            else:
                errors += 1
                if verbose:
                    print(f"{file_name} ✖")
        self._done(errors)

    def info(self, args):
        print(self.config)

    def setup(self, args, verbose=False):
        conf = Config()
        conf.setup()

        self.config = conf
        self.api_client = ApiClient(conf)
        if not self.api_client.ping():
            return

        conf.save_file()

    @staticmethod
    def _done(errors, overwrite=None, created=None):
        dst = f"done ✔✔✔ "

        if overwrite is not None:
            dst += f"(overwrite={overwrite}) "

        if created is not None:
            dst += f"(created={created}) "

        dst += f'(errors={errors})'
        print(dst)
