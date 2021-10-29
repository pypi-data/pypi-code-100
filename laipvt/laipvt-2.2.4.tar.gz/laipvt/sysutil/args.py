# -*- encoding: utf-8 -*-
import argparse


def Args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--force', dest="isCheck", action="store_true", default=False, help="前置检查效验")
    parser.add_argument('-f', '--targz-file', dest="targzFile", type=str, help="指定部署压缩包")
    parser.set_defaults(which='')

    subparsers = parser.add_subparsers(title='laipvt', description='命令模块分组', help='命令模块分组')

    deploy_parser = subparsers.add_parser('license', help='授权功能相关参数')
    deploy_parser.add_argument('--license-file', dest="LicenseFile",
                               type=str, help="指定需要更新的授权文件")
    deploy_parser.add_argument('--ocr-license-file', dest="OcrLicenseFile",
                               type=str, help="指定需要更新的ocr授权文件")
    deploy_parser.set_defaults(which='license')


    add_parser = subparsers.add_parser('deploy', help='部署额外功能相关参数')
    add_parser.add_argument('--monitor', dest="Monitor", action="store_true",
                                default=False, help="部署监控功能")
    add_parser.add_argument('--keepalive', dest="Keepalive", action="store_true",
                                default=False, help="部署keepalive服务")
    add_parser.set_defaults(which='add')


    delete_parser = subparsers.add_parser('delete', help='删除功能相关参数')
    delete_parser.add_argument("--docker", dest="Docker", action="store_true",
                                default=False, help="删除docker服务")
    delete_parser.add_argument('--kubernetes', dest="Kubernetes", action="store_true",
                                default=False, help="删除kubernetes服务")
    delete_parser.add_argument('--middleware', dest="Middleware", action="store_true",
                                default=False, help="删除middleware中间件服务")
    delete_parser.add_argument('--all', dest="All", action="store_true",
                                default=False, help="删除所有服务")
    delete_parser.set_defaults(which='delete')

    return parser


if __name__ == '__main__':
    args = Args().parse_args()
    print(args)
