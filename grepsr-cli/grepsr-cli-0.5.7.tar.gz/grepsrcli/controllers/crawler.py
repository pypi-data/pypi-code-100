from os import makedirs, system, path, stat
import time
import pathlib
from semver import VersionInfo
from cement import Controller, ex
from ..core.config import load_config
from ..core.utils import create_boilerplate, render_boilerplate, get_plugin_info, get_plugin_path, show_schema
from ..core.tech_local import TestLocal
from ..core.message_log import Log
from ..core.aws_s3 import S3


class CrawlerBase(Controller):
    class Meta:
        label = 'crawler_base'


class Crawler(Controller):
    config = load_config('config.yml')

    class Meta:
        label = 'crawler'
        stacked_on = 'crawler_base'
        stacked_type = 'nested'

    @ex(
        help="test a plugin locally",
        arguments=[
            (['-s'], {
                'action': 'store',
                'dest': 'plugin_name',
                'help': "The name of the service/plugin to run locally"
            }),
        ]
    )
    def test(self):

        plugin_name = self.app.pargs.plugin_name

        if get_plugin_path(plugin_name, type='php'):
            base_path = pathlib.Path(get_plugin_path(
                plugin_name, type='php')).parent
            TestLocal('php', plugin_name, base_path)
        elif get_plugin_path(plugin_name, type='php_next'):

            base_path = pathlib.Path(get_plugin_path(
                plugin_name, type='php_next')).parent
            TestLocal('php_next', plugin_name, base_path)
        else:
            self.app.log.error("path: {} not found!".format(plugin_name))

    @ex(
        help="performs git pull to update the codebase",
        arguments=[
            (['-t', '--type'], {
                'action': 'store',
                'dest': 'type',
                'help': "Platform type: php|node|python|php_next"
            })
        ]
    )
    def sync(self):
        if(self.app.pargs.type):
            type = self.app.pargs.type
            crawler_paths = self.config[type]['paths']

            for crawler_path in crawler_paths:
                Log.info(f"Syncing: {crawler_path}")
                system(
                    f"""cd {crawler_path}  && git pull origin master""")
        else:
            Log.warn("Please enter a valid type")

    @ex(
        help="create basic boilerplate for plugins ",
        arguments=[
            (['-s'], {
                "action": "store",
                "dest": "plugin_name",
                "help": "the name of the plugin to be created"
            }), (['-pid'], {
                "action": "store",
                "dest": 'pid',
                "help": "the project id of the plugin"
            }), (
                ['-t', '--template'], {
                    "action": "store",
                    "dest": 'template',
                    "help": "choose a template to boilerplate php|node|py|vc defaults to php"
                }
            ), (
                ['--path'], {
                    'action': "store",
                    'dest': 'folder_path',
                    'help': 'the path of the folder where the plugin will reside'
                }
            )
        ]
    )
    def create(self):

        template = self.app.pargs.template

        if self.app.pargs.folder_path is not None:
            folder_path = self.app.pargs.folder_path
            folder_path = folder_path.rstrip('/')
            folder_path = path.expanduser(folder_path)

        else:
            self.app.log.error(
                "cannot create boilerplate file without destination path")
            return

        if self.app.pargs.plugin_name is not None:
            plugin_name = self.app.pargs.plugin_name
        else:
            self.app.log.error(
                "cannot create boilerplate file without plugin's name")
            return

        if self.app.pargs.pid is not None:
            pid = self.app.pargs.pid
        else:
            pid = '***'

        data = {
            'plugin_name': plugin_name,
            'pid': pid
        }
        plugin_path = folder_path + '/' + plugin_name
        if template == 'vc':
            create_boilerplate(
                plugin_path, "php_vc_boilerplate.jinja2", data, 'php')

        elif template == 'py':
            create_boilerplate(
                plugin_path, "py_boilerplate.jinja2", data, 'py')

        elif template == 'node':
            create_boilerplate(
                plugin_path, "node_boilerplate.jinja2", data, 'js')
        else:
            create_boilerplate(
                plugin_path, "php_boilerplate.jinja2", data, 'php')

    @ex(
        help="deploy a specific plugin to live with versioning",
        arguments=[
            (['-s'], {
                "action": "store",
                "dest": 'plugin_name'
            }), (['-m'], {
                "action": "store",
                "dest": "message"
            }), (['-st', '--stable'], {
                "action": "store_true",
                "dest": "stable_flag"
            }), (['--patch'], {
                "action": "store_true",
                "dest": "patch_flag"
            }), (['--minor'], {
                "action": "store_true",
                "dest": "minor_flag",
                "help": "set major of a version"
            }), (['--major'], {
                "action": "store_true",
                "dest": "major_flag"
            })
        ]
    )
    def deploy(self):
        input_plugin_name = self.app.pargs.plugin_name
        deploy_message = self.app.pargs.message

        if input_plugin_name is None:
            self.app.log.error(
                "cannot deploy without service code")
            return False
        if deploy_message is None:
            self.app.log.error(
                "cannot deploy without deploy message")
            return False

        if self.app.pargs.stable_flag:
            deploy_type = "DEPLOY-STABLE"
        else:
            deploy_type = "DEPLOY"

        major_flag = self.app.pargs.major_flag
        minor_flag = self.app.pargs.minor_flag

        plugin_names = False
        if(',' in input_plugin_name):
            plugin_names = input_plugin_name.split(',')

        if(plugin_names == False):
            plugin_names = []
            plugin_names.append(input_plugin_name)

        for plugin_name in plugin_names:
            print(f'Initiating Deplyment for: {plugin_name} ')

            plugin_name = plugin_name.strip()

            plugin_dir_path = get_plugin_path(plugin_name, all_types=True)

            if(plugin_dir_path):
                # system(f"""
                # cd {plugin_dir_path} && 
                # cd .. &&
                # git pull 
                # """)
          
                plugin_info = get_plugin_info(plugin_dir_path)
                version_path = '{}/.version'.format(plugin_dir_path)
                if(path.exists(version_path)):
                    with open(version_path, 'r') as f:
                        version_info = VersionInfo.parse(f.read())
                        if(major_flag):
                            version_info = version_info.next_version(
                                part='major')
                        elif(minor_flag):
                            version_info = version_info.next_version(
                                part='minor')
                        else:
                            version_info = version_info.bump_patch()

                        version_info = str(version_info)
                        with open(version_path, 'w') as w:
                            w.write(version_info)

                    self.app.log.info(
                        "[{}] [{}] {}".format(deploy_type, version_info, deploy_message))
                else:
                    with open(version_path, 'w') as f:
                        if(major_flag):
                            version_info = "1.0.0"
                        elif (minor_flag):
                            version_info = "0.1.0"
                        else:
                            version_info = "0.0.1"

                        f.write(version_info)

                    self.app.log.info(
                        "[{}] [{}] {}".format(deploy_type, version_info, deploy_message))

                command = """
                cd {} &&
                cd .. &&
                git stash && 
                git pull origin master && 
                git stash pop && 
                git add {}/ &&
                git commit -m "[{}] [{}] {}" &&
                git push origin master
                """.format(plugin_dir_path, plugin_name, deploy_type, version_info, deploy_message)
                
                # sleep for 2 second to make it look real deployment
                time.sleep(2)

                show_schema(plugin_dir_path)

                system(command)
                # sleep for 2 second to make it look real deployment
                time.sleep(2)
                try:
                    app_url = f'https://appnext.grepsr.com/projects/{plugin_info["pid"]}'
                    self.app.log.info(f"App Url: {app_url}")
                    self.app.log.info(
                        f"Plugin: {plugin_name} deployed successfully")
                except:
                    self.app.log.warning(
                        f"Cannot find pid in plugin, please find the project's url manually")
                    self.app.log.info(
                        f"Plugin: {plugin_name} deployed successfully")
            else:
                self.app.log.error(f'plugin: {plugin_name} was not found')

    @ex(
        help="use a base plugin from: https://bitbucket.org/grepsr/vortex-plugins-services-base",
        arguments=[
            (['-s'], {
                "help": "name of the base crawler you want to use",
                "action": "store",
                "dest": "base_plugin_name"
            }),
            (['-t'], {
                "help": "name of target crawler that you want to use",
                "action": "store",
                "dest": "plugin_name"
            })
        ]
    )
    def use_basecrawler(self):

        s3 = S3()

        version = None
        base_plugin_name = self.app.pargs.base_plugin_name
        target_plugin_name = self.app.pargs.plugin_name

        if(base_plugin_name is None or target_plugin_name is None):
            Log.error(
                "Please Enter base crawler and target cralwers.\nUse gcli crawler use-basecrawler -h for more information")
            return

        if('-' in base_plugin_name):
            version = base_plugin_name.split('-')[1]
            base_plugin_name = base_plugin_name.split('-')[0]

        # to check if there is a base-plugin in thier gcli settings ...
        base_plugin_dir_path = get_plugin_path(
            base_plugin_name, type='php')

        target_plugin_path = get_plugin_path(
            target_plugin_name, type='php'
        )

        if(version is None and base_plugin_dir_path):
            f = open(f"{base_plugin_dir_path}/.version", mode='r')
            version = f.read()
            f.close()

        if(version is None):
            Log.error(
                "Please Specify the version of base crawler that you want to use")
            return

        if(target_plugin_path):
            Log.info(
                f'Getting Secure Url of target plugin: {base_plugin_name}, {version}')

            presigned_url = s3.get_secure_url(bucket='crawler-plugins',
                                              filename=f'php/vortex-plugins-services-base/{base_plugin_name}/{base_plugin_name}-{version}.tar.gz')
            data = {
                'presigned_url': presigned_url,
                'plugin_name': base_plugin_name,
                'version': version
            }

            render_boilerplate(boilerplate='composer.jinja2', data=data,
                               destination_path=target_plugin_path + '/composer.json')
            system(
                f""" cd {target_plugin_path} &&  composer install""")
        else:
            Log.error(f"Target plugin: {target_plugin_name} not found")