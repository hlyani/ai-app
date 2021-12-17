import paramiko
import subprocess
import sys
import os
import time
from app.config import Config, argparse_handle
from app.log import logger


LOG = logger()
args = argparse_handle()
config = Config()
config.read_from_file(args.get("conf_path"))


class SSH:
    def __init__(self):
        self.host = config.get("default", "host")
        self.port = config.get("default", "port", "int")
        self.user = config.get("default", "user")
        self.password = config.get("default", "password")
        self.ssh_key_path = config.get("default", "ssh_key_path")
        self.timeout = config.get("default", "timeout", "int")

        self.out_password = os.getenv("PASSWORD") if os.getenv(
            "PASSWORD") else config.get("default", "out_password")
        self.out_user = os.getenv("USERNAME") if os.getenv(
            "USERNAME") else config.get("default", "out_user")
        self.out_host = os.getenv("IP") if os.getenv(
            "IP") else config.get("default", "out_host")
        self.out_path = os.getenv("DESTINATIONPATH") if os.getenv(
            "DESTINATIONPATH") else config.get("default", "out_path")
        self.in_path = os.getenv("SOURCEPATH") if os.getenv(
            "SOURCEPATH") else config.get("default", "in_path")
        self.connect()

    def connect(self):
        # 创建 ssh 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 known_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        # 获取私钥
        pkey = paramiko.RSAKey.from_private_key_file(
            self.ssh_key_path) if self.ssh_key_path else None
        # 连接服务器
        ssh.connect(hostname=self.host,
                    port=self.port if self.port else 22,
                    username=self.user,
                    password=self.password,
                    timeout=self.timeout if self.timeout else 1800,
                    pkey=pkey)
        self.ssh = ssh

    def exec(self, shell):
        LOG.info("Executing command...")
        LOG.info("[%s]" % shell)
        # print("Executing command...")
        # print("[%s]" % shell)
        # 执行命令
        stdin, stdout, stderr = self.ssh.exec_command(
            command=shell,
            bufsize=1,
            timeout=self.timeout if self.timeout else 1800)
        # 获取命令结果
        lines = ""
        while True:
            line = stdout.readline()
            if not line:
                break
            lines = lines + line
        LOG.info(lines)
        # print(lines)
        err = bytes.decode(stderr.read())
        if err:
            LOG.error("Failed to execute command:", err)
            # print("Failed to execute command:", err)
            self.close()
        LOG.info("Complete execute command.")
        # print("Complete execute command.")

    def close(self):
        # 关闭连接
        self.ssh.close()

    def cp_file(self, src, dest):
        LOG.info("Transferring file...")
        # print("Transferring file...")
        cmd = "sshpass -p {pwd} scp -o StrictHostKeyChecking=no -r -P {port} {src} {user}@{host}:{dest}" \
            .format(pwd=self.password,
                    port=self.port if self.port else 22,
                    src=src,
                    user=self.user,
                    host=self.host,
                    dest=dest)
        err, _ = localShell(cmd)
        if err:
            LOG.error("Failed to transfer file: ", err)
            # print(Failed to transfer file:", err)
            sys.exit(1)
        LOG.info("Complete file transfer.")
        # print("Complete file transfer.")


def localShell(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, shell=True)
    results = popen.stdout.read()
    popen.stdout.close()
    return_code = popen.wait()
    err = None
    if return_code:
        err = str(subprocess.CalledProcessError(return_code, cmd))
    return err, results


def isFile(path):
    return os.path.exists(path)


def main():
    s = SSH()
    path = "/opt/app/*.tgz /opt/app/*.sh"
    # path = "./ai_app/colorization.*"
    # path = "./ai_app/classification.*"
    s.cp_file(path, "/home/HwHiAiUser/")
    s.exec("OUT_PASSWORDD=%s OUT_USER=%s OUT_HOST=%s OUT_PATH=%s IN_PATH=%s bash /home/HwHiAiUser/*.sh" %
           (s.out_password, s.out_user, s.out_host, s.out_path, s.in_path))
    s.close()
    while True:
        LOG.info("Waiting to exit...")
        # print("Waiting to exit.")
        time.sleep(3600)


if __name__ == "__main__":
    main()
