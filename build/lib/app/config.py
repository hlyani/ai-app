import configparser
import argparse
import os


class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()

    def read_from_file(self, filepath):
        self.config.read(filepath)

    def get(self, section, option, type="string"):
        if not self.config.has_option(section, option):
            return None
        if type == "int":
            return self.config.getint(section, option)
        elif type == "boolean":
            return self.config.getboolean(section, option)
        elif type == "float":
            return self.config.getfloat(section, option)
        else:
            return self.config.get(section, option)


# 命令行启动时参数解析
def argparse_handle():
    """
    :return: {
        "conf_path": "<conf_path>", # 配置文件路径
    }
    """
    result = {}
    # 默认配置文件路径
    conf_path = ""
    default_conf_path = ""
    if os.path.isfile("/opt/app/app.conf"):
        default_conf_path = "/opt/app/app.conf"
    else:
        default_conf_path = "./app.conf"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--conf", "-f",
        help="Specify the configuration file path."
        "Default is '{0}'".format(default_conf_path)
    )
    args = parser.parse_args()

    # 确认配置文件路径
    if args.conf:
        conf_path = args.conf
    else:
        if os.path.isfile(default_conf_path):
            conf_path = default_conf_path
    if not conf_path:
        raise Exception("No avaliable configuration file found."
                        "Plaese use -h to display usage.")

    result["conf_path"] = conf_path

    return result
