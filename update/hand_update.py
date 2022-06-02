"""######################
Author: Nguyen Dinh Hai
Ver:    0.0
Date: 06/01/2021
#####################"""

from swagger_client import VersionSeverApi, VersionApi, AccountApi
from swagger_client import ApiClient
from decouple import config

import subprocess
import schedule
import logging
import os
import shutil
import time
import json
import configparser


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')

# Load file config
config_inf = configparser.RawConfigParser()

try:
    config_inf.read('config.cfg')
    details_dict = dict(config_inf.items('CONFIG_IMAGE'))

    # Get two param max width and max height from config file
    EMAIL = details_dict['email']
    PASSWORD = details_dict['password']

except Exception as e:
    logging.info(e)


# Get token from authn function
def get_authToken():
    email = EMAIL
    password = PASSWORD

    try:
        myAaccount = AccountApi().account_login(credentials={"email": email, "password": password})
        apiCLI = ApiClient(header_name='Authorization', header_value=myAaccount['id'])
        return apiCLI
    except Exception as error:
        logging.info(error)
        return False


def convert_authen(url, user='', password=''):
    """
    Detail: Convert link to authen in git
    :param url:
    :param user:
    :param password:
    :return:
    """

    if "https://" not in url:
        logging.info(f"Please check {url}, url must have https://")
        return False

    if not user or not password:
        logging.info(f"please check password or user")
        return False

    if "@" in user or "@" in password:
        logging.info("password or user format is wrong, can not have @ digit")

    tmp_url = url.split("https://")
    if len(tmp_url) < 2:
        logging.info("url format not True")
        return False

    tmp = ''
    authen_url = "https://" + f"{user}:{password}@" + tmp.join(tmp_url)
    return authen_url


class Git:

    repo_remote = [{"repo": "SUNNY_CREATE_VIDEO", "file": ["./.env"]},
                   {"repo": "VIDEO_GENERATION", "file": ["./.env"]},
                   {"repo": "SUNNY_MAKE_VIDEO_FL_TEMPLATE", "file": ["./.env"]},
                   {"repo": "youtube-node", "file": ["./src/config.ts", "./.env"]},
                   {"repo": "UPLOAD_VIDEO_MANUAL", "file": ["./src/config.ts", "./.env"]}]
    url_remote = ''
    repo_name = ''

    def __init__(self, user='', password=''):
        self.user = user
        self.password = password

    def get_remote_url(self):
        process = subprocess.run("git remote -v", shell=True, stdout=subprocess.PIPE)
        _out_cmd = process.stdout
        _output = _out_cmd.decode('utf-8').splitlines()
        if len(_output) == 0:
            logging.info("Cannot decode success")
            return False

        Git.url_remote = _output[0].split(".git")[0].split("origin\t")[-1]
        Git.repo_name = Git.url_remote.split("/")[-1]
        # print(Git.url_remote)

    # def get_data(self):
    def get_authen(self):
        if not Git.url_remote:
            logging.info(f"Please check {Git.url_remote}, url must have https://")
            return False

        if "https://" not in Git.url_remote:
            logging.info(f"Please check {Git.url_remote}, url must have https://")
            return False

        if not self.user or not self.password:
            logging.info(f"please check password or user")
            return False

        if "@" in self.user or "@" in self.password:
            logging.info("password or user format is wrong, can not have @ digit")
            return False

        tmp_url = self.url_remote.split("https://")
        if len(tmp_url) < 2:
            logging.info("url format not True")

        tmp = ''
        Git.url_remote = "https://" + f"{self.user}:{self.password}@" + tmp.join(tmp_url)
        print(Git.url_remote)

    def git_pull(self):
        check_status = False
        path_temp = ''
        _files_path = ''
        _repo_name = ''

        for repo in Git.repo_remote:
            if repo["repo"] in Git.url_remote:
                _files_path = repo['file']
                _repo_name = repo["repo"]
                path_temp = f"../tempo/{repo['repo']}"

                for _file_path in _files_path:
                    _file_name = _file_path.split('/')[-1]

                    if os.path.isfile(_file_path):
                        check_status = True
                        if not os.path.isdir(path_temp):
                            if not os.path.isdir("../../tempo"):
                                try:
                                    os.mkdir("../../tempo")
                                except Exception as e:
                                    logging.info(e)

                            try:
                                os.mkdir(path_temp)
                            except Exception as e:
                                logging.info(e)
                                return False

                    try:
                        shutil.move(_file_path, f"{path_temp}/{_file_name}")
                    except Exception as e:
                        logging.info(e)
                        return False
                break

        process = subprocess.run(f"git pull {Git.url_remote}", shell=True, stdout=subprocess.PIPE)
        _out_cmd = process.stdout
        _outputs = _out_cmd.decode('utf-8').splitlines()

        if check_status:
            for _file_path in _files_path:
                _file_name = _file_path.split('/')[-1]
                try:
                    shutil.move(f"{path_temp}/{_file_name}", _file_path)
                except Exception as e:
                    logging.info(e)
                    logging.info(f"You maybe must move file {_file_name} to origin folder by hand")
                    return False

        if _outputs[-1] == "Already up to date.":
            logging.info("Nothing need to update")
            return True

        for _output_ in _outputs:
            if "error:" in _output_:
                logging.info(f"Can not pull code git log:\n{_out_cmd.decode('utf-8')}")
                return False

        logging.info("Success")

    def get_version(self):
        check_status = False
        path_temp = ''
        _file_path = ''
        _file_name = ''
        _repo_name = ''
        repo_name = ''

        for repo in Git.repo_remote:

            if repo["repo"] in Git.url_remote:
                repo_name = repo["repo"]
                path_temp = f"../tempo/{repo['repo']}"

                if os.path.isfile(_file_path):
                    check_status = True
                    if not os.path.isdir(path_temp):
                        if not os.path.isdir("../../tempo"):
                            try:
                                os.mkdir("../../tempo")
                            except Exception as e:
                                logging.info(e)

                        try:
                            os.mkdir(path_temp)
                        except Exception as e:
                            logging.info(e)
                            return False

                break

        log_file = f"{path_temp}/version.json"
        version = 0

        if os.path.isfile(log_file):
            try:
                with open(log_file) as json_file:
                    data = json.load(json_file)
                version = int(data['id'])
            except Exception as error:
                logging.info(error)

        return version, repo_name, log_file


def main():
    user = 'release'
    password = 'Abc00102030'
    apiCLI = get_authToken()

    try:
        server_str = config("SERVER")
        SERVER_IDS = server_str.split(",")
    except:
        logging.info("Can not get servers from ./.env")
        return False

    if not apiCLI:
        logging.info("Can not get authToken to api")
        return False

    try:
        notice_versionApi = VersionApi(api_client=apiCLI)
        version_Api = VersionSeverApi(api_client=apiCLI)
    except Exception as e:
        logging.info(e)
        return False

    # Fist value for varaiable
    version_server = 0
    version_local = 0
    repo_name = ''
    log_file = ''

    # Use class git
    git = Git(user=user, password=password)
    # Get link remote repo
    git.get_remote_url()
    # convert link to use auth
    git.get_authen()

    # Get version, repo name and path of log file version in local
    try:
        version_local, repo_name, log_file = git.get_version()
    except Exception as e:
        logging.info(e)

    # # Check version in server
    # filter = json.dumps({"where": {'nameOfService': repo_name,
    #                                'serverId': {'inq': SERVER_IDS}},
    #                      "order": 'id DESC'
    #                      })
    # versions = version_Api.version_sever_find(filter=filter)

    version_server = 1
    version_local = 0

    # if len(versions) != 0:
    #     version_server = versions[0].id
    # else:
    #     logging.info("No version need update could be found in server")
    #     return False

    if version_server == 0 and version_local == 0:
        pass

    elif version_server <= version_local:
        return False

    # Git pull
    git.git_pull()

    time.sleep(5)

    _data = {'repoUrl': f'https://git.vfast.live/VFAST/{repo_name}',
             'nameOfService': repo_name,
             'version': version_server
             }

    data = json.dumps(_data)

    try:
        notice_versionApi.version_create(data=_data)
    except Exception as e:
        logging.info(e)

    try:
        with open(log_file, 'w') as f:
            f.truncate()
            f.write(data)
            f.close()
    except Exception as e:
        logging.info(e)

    time.sleep(20)
    files_lib = os.listdir("../outside_lib")

    if len(files_lib) == 0:
        pass

    else:
        for file_name in files_lib:
            if "image_processing" in file_name:
                subprocess.run(f"pip3 install ./outside_lib/{file_name}", shell=True)

    time.sleep(10)
    subprocess.run("make restart", shell=True)


if __name__ == "__main__":
    main()
