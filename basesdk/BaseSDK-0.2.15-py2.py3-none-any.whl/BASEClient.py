import requests
import logging
import os

from BaseSDK import Utils
from BaseSDK.Configuration import *
from BaseSDK.ClientException import ResourceException, AuthException

from multiprocessing import Pool

import json
import hashlib


url_dict = {
    'get_dataset':'/sdk/datasets/{sampleset_id}/files',
    'get_sampleset': '/sdk/samplesets/{sampleset_id}/files',
    'get_labels': '/sdk/labels',
    'get_categories': '/sdk/category',
    'get_model_upload_url': '/sdk/models/{model_name}/upload',
    'get_log_upload_url': '/sdk/log/upload',
    'get_pretrain': '/model-store/pretrain-models/{model_name}',
    'get_model': '/sdk/models/{model_id}',
    'get_callback_upload_model':'/sdk/models/upload',
}


class BASEClient(metaclass=Singleton):
    def __init__(self, apiKey=None, context='prod'):
        self.logger = logging.getLogger('BASEClient')
        self.config = Configuration(context)
        self.apiKey = apiKey

    def get_dataset_files(self, sampleset_id, sensor='all'):
        """

        Args:
            sampleset_id: id of the sampleset to route to the dataset to download
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            files: file list
        """
        payload = {
            'sensor': sensor
        }
        url = self.config.url + url_dict.get('get_dataset').format(sampleset_id=sampleset_id)
        try:
            dataset_resp = requests.get(url=url,
                                        params=payload,
                                        headers={'apiKey': self.apiKey})

            if dataset_resp.status_code == 200:
                content = dataset_resp.json()
                if content['code'] == 200:
                    return content['data']
                else:
                    raise ResourceException(content['msg'])
            else:
                raise AuthException(dataset_resp.reason)
        except Exception as e:
            raise e

    def download_dataset(self, sampleset_id, save_path, sensor='all'):
        """

        Args:
            sampleset_id: id of the sampleset to route to the dataset to download
            save_path: local path to save the files
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            True if the dataset files downloaded successfully.
        """
        Utils.makedir(save_path)
        sensors = self.get_dataset_files(sampleset_id, sensor)
        if not sensors:
            self.logger.error("No sensors found in the dataset.")
            return False

        for sensor, files in sensors.items():
            data = [[os.path.join(save_path, _file['filename']), _file['url']] for _file in files]
            with Pool(5) as pool:
                pool.map(Utils.download_binary, data)

        return True

    def get_sampleset_files(self, sampleset_id, sensor='all'):
        """

        Args:
            sampleset_id: id of the sampleset to download
            batch: the batch name of the sampleset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            files: file list
        """
        payload = {
            'sensor': sensor
        }
        url = self.config.url + url_dict.get('get_sampleset').format(sampleset_id=sampleset_id)
        try:
            sampleset_resp = requests.get(url=url,
                                        params=payload,
                                        headers={'apiKey': self.apiKey})

            if sampleset_resp.status_code == 200:
                content = sampleset_resp.json()
                if content['code'] == 200:
                    return content['data']
                else:
                    raise ResourceException(content['msg'])
            else:
                raise AuthException(sampleset_resp.reason)
        except Exception as e:
            raise e

    def download_sampleset(self, sampleset_id, save_path, sensor='all'):
        """

        Args:
            sampleset_id: id of the sampleset to download
            save_path: local path to save the files
            batch: the batch name of the sampleset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            True if the sampleset files downloaded successfully.
        """
        Utils.makedir(save_path)
        sensors = self.get_sampleset_files(sampleset_id, sensor)
        if not sensors:
            self.logger.error("No sensors found in the sampleset.")
            return False

        for sensor, files in sensors.items():

            data = [[os.path.join(save_path, _file['filename']), _file['url']] for _file in files]
            with Pool(5) as pool:
                pool.map(Utils.download_binary, data)

        return True

    def get_label_files(self, sampleset_id, sensor='all'):

        payload = {
            'sensor': sensor
        }
        url = self.config.url + url_dict.get('get_sampleset').format(sampleset_id=sampleset_id)
        try:
            label_resp = requests.get(url=url,
                                        params=payload,
                                        headers={'apiKey': self.apiKey})

            if label_resp.status_code == 200:
                content = label_resp.json()
                if content['code'] == 200:
                    return content['data']
                else:
                    raise ResourceException(content['msg'])
            else:
                raise AuthException(label_resp.reason)
        except Exception as e:
            raise e


    def request_save_label(self, args):
        sampleset_id, sensor, filename, save_path = args
        payload = {
            'sampleSetId': sampleset_id,
            'sensor': sensor,
            'fileName': filename
        }
        try:
            label_resp = requests.get(url=self.config.url + url_dict.get('get_labels'),
                                        params=payload,
                                        headers={'apiKey': self.apiKey}).json()
            label_info = label_resp['data']
            json_file_name = os.path.join(save_path, filename.split('.')[0] + '.json')
            with open(json_file_name, 'w') as handle:
                json.dump(label_info, handle)
        except Exception as e:
            raise e
            
            
    def download_labels(self, sampleset_id, save_path, sensor='all', ):
        """

        Args:
            sampleset_id: id of the sampleset to download
            save_path: local path to save the files
            batch: the batch name of the sampleset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
             True if the sampleset files downloaded successfully.
        """
        Utils.makedir(save_path)
        sensors = self.get_label_files(sampleset_id, sensor)
        if not sensors:
            self.logger.error("No sensors found in the sampleset.")
            return False
        for sensor, files in sensors.items():
            args = [[sampleset_id, sensor, file['filename'], save_path] for file in files]
            with Pool(5) as pool:
                pool.map(self.request_save_label, args)
        return True

    def get_categories(self, sampleset_id):
        """
        Args:
            sampleset_id: id of the sampleset that the

        Returns:

        """
        try:
            payload = {
                'samplesetId': sampleset_id,
            }
            category_resp = requests.get(
                url=self.config.url + url_dict.get('get_categories'),
                params=payload,
                headers={'apiKey': self.apiKey}).json()
            if category_resp['code'] == 200:
                _categories = category_resp['data']['categories']
                return [cate['name'] for cate in _categories]
            else:
                raise ResourceException(category_resp['msg'])
        except Exception as e:
            raise e

    def upload_model(self, task_id, model_name, model_file):
        """

        Args:
            task_id: unique id of the task
            model_name: model unique name
            model_file: file path of the serializers model to upload

        Returns:
            True if upload successfully.
        """

        try:
            md5 = self.calculate_md5(model_file)
            payload = {
                "taskId":task_id,
                "md5":md5
            }
            upload_resp = requests.get(url=self.config.url + url_dict.get('get_model_upload_url').format(model_name=model_name),
                                       params=payload,
                                       headers={'apiKey': self.apiKey}).json()

            if upload_resp['code'] != 200:
                self.logger.warning(upload_resp['msg'])
                return

            url = upload_resp['data']['key']

            with open(model_file, 'rb') as file_to_upload:
                upload_response = requests.put(url=url, data=file_to_upload)

            self.logger.info(upload_response)

            return True

        except Exception as e:
            raise e

    def upload_log(self, task_id, model_name, log_file):
        """

        Args:
            task_id: unique id of the task
            model_name: model unique name
            log_file: file path of log to upload

        Returns:
            True if upload successfully.
        """

        try:
            payload = {
                "taskId":task_id,
                "modelName":model_name
            }
            upload_resp = requests.get(url=self.config.url + url_dict.get('get_log_upload_url'),
                                       params=payload,
                                       headers={'apiKey': self.apiKey}).json()

            if upload_resp['code'] != 200:
                self.logger.warning(upload_resp['msg'])
                self.logger.warning('request for uploading log file failed')
                return

            url = upload_resp['data']['key']
            print(url)

            with open(log_file, 'rb') as file_to_upload:
                upload_response = requests.put(url=url, data=file_to_upload)

            self.logger.info(upload_response)

            return True

        except Exception as e:
            raise e

    def upload_label(self, label):
        """

        Args:
            label: the result of the model inference in json format

        Returns:
            True if upload successfully.
        """
        try:
            upload_resp = requests.post(
                url=self.config.url + url_dict.get('get_labels'),
                data=label,
                headers={'apiKey': self.apiKey,'Content-Type':'application/json'}).json()

            if upload_resp['code'] != 200:
                self.logger.warning(upload_resp['msg'])
                return

            self.logger.info(upload_resp['code'])
            return True

        except Exception as e:
            raise e


    def download_pretrain(self, model_name, save_path):
        """
        Args:
            model_name: model unique name
            save_path: local path to save the files

        Returns:
            True if download successfully.
        """
        try:
            Utils.makedir(save_path)
            # url = self.config.endpoint + url_dict.get("get_pretrain").format(model_name=model_name)
            url = 'http://192.168.0.111:30197/model-store/pretrain-models/ddrnet.pth?Content-Disposition=attachment%3B%20filename%3D%22pretrain-models%2Fddrnet.pth%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=boden%2F20210930%2F%2Fs3%2Faws4_request&X-Amz-Date=20210930T060339Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=db216f6792d90a3377135a85130f385baa2f4e6ce1f070b58439ee6c0c081292'
            # payload = {"model_name": model_name}
            # header = {'apiKey': self.apiKey}
            # pretrain_resp = requests.get(url, params=payload, headers=header).json()
            pretrain_resp = requests.get(url)
            # if pretrain_resp['code'] != 200:
            #     self.logger.warning(pretrain_resp['msg'])
            #     return
            # data = (os.path.join(save_path, "{}.pth".format(model_name)), pretrain_resp['url'])
            data = (os.path.join(save_path, "{}.pth".format(model_name)), url)
            Utils.download_binary(data)
            return True

        except Exception as e:
            raise e

    def get_model(self, model_id):
        """
        Args:
            task_id: the unique id of the task

        Returns:
            model information.
        """
        try:
            header = {'apiKey': self.apiKey}
            model_resp = requests.get(url=self.config.url + url_dict.get("get_model").format(model_id=model_id),headers=header).json()
            if model_resp['code'] != 200:
                self.logger.warning(model_resp['msg'])
                raise ResourceException(model_resp['msg'])

            return model_resp['data']

        except Exception as e:
            raise e


    def download_model(self, model_id, save_path):
        """
        Args:
            model_id: the unique id of the model
            model_name: model unique name
            save_path: local path to save the files

        Returns:
            True if download successfully.
        """
        try:
            Utils.makedir(save_path)
            model_resp = self.get_model(model_id)
            model_url = model_resp['modelUrl']
            md5 = model_resp['md5']
            save_path =os.path.join(save_path, "{}.pth".format('pretrain'))
            data = (save_path, model_url)
            Utils.download_binary(data)
            md5_ = self.calculate_md5(save_path)
            if md5 == md5_:
                return True
            else:
                raise Exception('the md5 of downloaded file is not match that in database!!!')
        except Exception as e:
            raise e

    def callback_upload_model(self, task_id, upload_success=False):
        try:
            if upload_success:
                payload = {
                    'taskId':task_id,
                    'status':1
                }
            else:
                payload = {
                    "taskId":task_id,
                    "status":0
                }
            payload = json.dumps(payload)
            resp = requests.post(url=self.config.url + url_dict.get('get_callback_upload_model'),
                                 data=payload, headers={'apiKey': self.apiKey,'Content-Type':'application/json'}).json()
            if resp['code'] != 200:
                self.logger.warning(resp['msg'])
                return

            self.logger.info(resp['code'])
            return True
        except Exception as e:
            raise e

    def calculate_md5(self, file_path):
        try:
            md5_hash = hashlib.md5()
            with open(file_path,'rb') as f:
                for byte_block in iter(lambda: f.read(4096),b""):
                    md5_hash.update(byte_block)
            return md5_hash.hexdigest()
        except Exception as e:
            raise e

if __name__ == '__main__':

    token = ""
    sampleset_id = ""
    c = BASEClient(token, "dev")  # "prod"

