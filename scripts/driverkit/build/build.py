#!/usr/bin/env python3

import sys
import os
import yaml
import shutil
import argparse
import pathlib
import subprocess
from pathlib import Path

# change 2

def driverkit_build(driverkit: str, config_file: Path, driverversion: str, devicename: str, drivername: str) -> bool:
    args = [driverkit, 'docker',
            '-c', str(config_file.resolve()),
            '--driverversion', driverversion,
            '--moduledevicename', devicename,
            '--moduledrivername', drivername,
            '--timeout', '1000']
    print('[*] {}'.format(' '.join(args)))
    status = subprocess.run(args)

    return status.returncode == 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config_dir', help='The directory containing driverkit config files, organized as <driver_version>/<configN>.yaml')
    ap.add_argument('--driverkit', help='Path to the driverkit binary to use')
    ap.add_argument('--s3-bucket', help='The S3 bucket name')
    ap.add_argument('--s3-prefix', help='S3 key prefix')
    args = ap.parse_args()

    config_dir = Path(args.config_dir)
    if not config_dir.exists():
        print(f"[-] config directory does not exist: {config_dir}")
        return 1

    driverkit = shutil.which('driverkit')
    if args.driverkit is not None:
        driverkit = args.driverkit

    if driverkit is None:
        print(f"[-] driverkit not found. Select the driverkit binary with --driverkit")
        return 1

    if not os.path.exists(driverkit):
        print(f"[-] driverkit binary {driverkit} does not exist")
        return 1

    dri_dirs = [x for x in config_dir.iterdir() if x.is_dir()]
    for dri_dir in dri_dirs:
        driverversion = dri_dir.name
        print(f"[*] loading drivers from driver version directory {driverversion}")
        files = list(dri_dir.glob("*.yaml"))
        print(f"[*] found {len(files)} files")

        count = 0
        success_count = 0
        fail_count = 0
        for config_file in files:
            count += 1
            print('[*] [{:03d}/{:03d}] {}'.format(count, len(files), config_file.name))

            with open(config_file) as fp:
                conf = yaml.safe_load(fp)

            module_output = conf.get('output', {}).get('module')
            probe_output = conf.get('output', {}).get('probe')
            
            # this needs to change if we have s3 or not
            need_module = (module_output is not None) and not os.path.exists(module_output)
            need_probe = (probe_output is not None) and not os.path.exists(probe_output)

            need_build = need_module or need_probe
            if not need_build:
                print('[*] {} already built'.format(config_file))
                continue

            # Make sure the output directory exists or driverkit will output "open: no such file or directory"
            if module_output is not None:
                Path(module_output).parent.mkdir(parents=True, exist_ok=True)
            if probe_output is not None:
                Path(probe_output).parent.mkdir(parents=True, exist_ok=True)

            success = driverkit_build(driverkit, config_file, driverversion, "sysdig", "sysdig-probe")
            if success:
                print('[+] Build completed {}'.format(config_file))
                success_count += 1
            else:
                print('[-] Build failed    {}'.format(config_file))
                fail_count += 1

        print(f"[*] Build {driverversion} complete. {success_count}/{count} built, {fail_count}/{count} failed.")

    return 0

if __name__ == '__main__':
    sys.exit(main())
