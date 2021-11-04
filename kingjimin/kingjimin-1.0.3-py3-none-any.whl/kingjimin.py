import requests
import contextlib
import polling2
from urllib.parse import urljoin
import json

class ApiClass():
    def __init__(self, address):
        self.address = address

    def check_status(self, res):
        status_code = res.status_code
        if status_code >= 400: # More than 400 is seen as an issue on the device farm side.
            print(f"Status code: {status_code}, Try again.")
            print(res.content)
            return False
        else:
            return True

    def _poll(self, add_str, method, files=None, params=None, headers=None):
        try:
            if(method == "get"):
                res = polling2.poll(
                    lambda: requests.get(
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=params,
                        headers=headers
                    ),
                    check_success = self.check_status,
                    step=5,
                    timeout=600) 
            else:
                res = polling2.poll(
                    lambda: requests.post(
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=params,
                        headers=headers
                    ),
                    check_success = self.check_status,
                    step=5,
                    timeout=600)
        except polling2.TimeoutException as e:
            print(e)
        return res

    def get_all_nodes(self):
        return self._poll(f"nodes", "get")

    def get_node_info(self, node_uuid):
        return self._poll(f"nodes/{node_uuid}", "get")

    def get_node_tasks(self, node_uuid):
        return self._poll(f"nodes/{node_uuid}/tasks", "get")

    def get_task(self, task_uuid):
        return self._poll(f"tasks/{task_uuid}", "get")

    def all_models(self):
        return self._poll(f"models", "get")

    def get_model_info(self, model_uuid):
        return self._poll(f"models/{model_uuid}", "get")

    def get_available_nodes(self, model_uuid):
        return self._poll(f"models/{model_uuid}/available_nodes", "get")

    def delete_model(self, model_uuid):
        """Delete_model."""
        return self._poll(f"models/{model_uuid}/delete", "post")

    def delete_only_model(self, model_uuid):
        return self._poll(f"models/{model_uuid}/delete_model_file", "post")

    def upload_model(self, model_path, output_model_type):
        """Upload_model."""
        paths = {"model": model_path}
        params = {"type": output_model_type}
        with contextlib.ExitStack() as stack:
            files = {
                n: stack.enter_context(open(p, "rb")) for n, p in paths.items() if p
            }
            return self._poll("upload_model", "post", files, params)

    def download_model(self, model_uuid):
        return self._poll(f"models/{model_uuid}/download", "get")

    def start_benchmark(self, model_uuid, node_uuid, benchmark_args) -> str:
        headers = {
            'Content-Type': 'application/json'
        }
        benchmark_args["node_uuids"] = [node_uuid]
        print(benchmark_args)
        params = json.dumps(benchmark_args)
        return self._poll(f"models/{model_uuid}/request_benchmark", "post", params=params, headers=headers)

    def all_benchmarks_on_model(self, model_uuid):
        return self._poll(f"models/{model_uuid}/benchmarks", "get")

    def benchmarks_on_model(self, model_uuid, bench_uuid):
        return self._poll(f"models/{model_uuid}/benchmarks/{bench_uuid}", "get")

    def delete_benchmark(self, model_uuid, bench_uuid):
        return self._poll(f"models/{model_uuid}/benchmarks/{bench_uuid}/delete", "post")