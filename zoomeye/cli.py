#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Filename: cli.py
* Description: cli program entry
* Time: 2020.11.30
* Author: liuf5
*/
"""

import os
import sys
import argparse

# os.path.realpath(__file__) 文件的绝对路径  eg:C:\knownsec\study\test.7.29.py
# os.path.dirname(os.path.realpath(__file__)) 文件所在目录的目录名  eg:C:\knownsec\study
# os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  目录所在的目录名 eg: C:\knownsec    ZoomEye-python/zoomeye
module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path 是一个列表
# 实际项目中，把自己项目所在的地址放在sys.path列表里面，便于快速导入模块
sys.path.insert(1, module_path)

from zoomeye import core
# 导入了那个大图片
from zoomeye.config import BANNER


def get_version():
    """
    获取版本的时候打印这个大图片
    """
    print(BANNER)


class ZoomEyeParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


def main():
    """
    parse user input args
    :return:
    """

    # ZoomEyeParser inherit argparse. ArgumentParser, have same init method
    # prog: program name
    parser = ZoomEyeParser(prog='zoomeye')
    # argparse add subparse object
    subparsers = parser.add_subparsers()
    # show ZoomEye-python version number
    # -v or --version optional argument
    # action: trigger -v or --version true, else false
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="show program's version number and exit"
    )

    # zoomeye account info
    # info argument binding core.info
    parser_info = subparsers.add_parser("info", help="Show ZoomEye account info")
    parser_info.set_defaults(func=core.info)

    # query zoomeye data
    # name or flags - 选项字符串的名字或者列表，例如foo或者 - f, --foo。
    # metavar - 在 usage 说明中的参数名称，对于必选参数默认就是参数名称，对于可选参数默认是全大写的参数名称.
    # const - action 和 nargs 所需要的常量值。
    # action - 命令行遇到参数时的动作，默认值是 store。
    # nargs - 应该读取的命令行参数个数，可以是具体的数字，或者是?号，当不指定值时对于 Positional argument 使用 default，
    #   对于 Optional argument 使用 const；或者是 * 号，表示 0 或多个参数；或者是 + 号表示 1 或多个参数。
    parser_search = subparsers.add_parser("search", help="Search the ZoomEye database")
    parser_search.add_argument("dork", help="The ZoomEye search keyword or ZoomEye exported file")
    parser_search.add_argument("-num", default=20,
                               help="The number of search results that should be returned, support 'all'", type=str,
                               metavar='value')
    parser_search.add_argument("-facet", default=None, nargs='?', const='country', type=str,
                               help=('''
                                    Perform statistics on ZoomEye database,
                                    host field: [app,device,service,os,port,country,city]
                                    web field: [webapp,component,framework,server,waf,os,country]
                                    '''), metavar='field'
                               )
    parser_search.add_argument(
        "-filter",
        default=None,
        metavar='field=regexp',
        nargs='?',
        const='app',
        type=str,
        help=('''
              Output more clearer search results by set filter field,
              host field: [app,version,device,port,city,country,asn,banner,timestamp,*]
              web field: [app,headers,keywords,title,site,city,country,webapp,component,framework,server,waf,os,timestamp,*]
        ''')
    )
    parser_search.add_argument(
        '-stat',
        default=None,
        metavar='field',
        nargs='?',
        const='app,device,service,os,port,country,city',
        type=str,
        help=('''
              Perform statistics on search results,
              host field: [app,device,service,os,port,country,city]
              web field: [webapp,component,framework,server,waf,os,country]
        ''')
    )
    parser_search.add_argument(
        "-save",
        default=None,
        metavar='field=regexp',
        help=('''
              Save the search results with ZoomEye json format,
              if you specify the field, it will be saved with JSON Lines
        '''),
        nargs='?',
        type=str,
        const='all'
    )
    parser_search.add_argument(
        "-count",
        help="The total number of results in ZoomEye database for a search",
        action="store_true"
    )
    parser_search.add_argument(
        "-figure",
        help="Pie chart or bar chart showing data，can only be used under facet and stat",
        choices=('pie', 'hist'),
        default=None
    )
    parser_search.add_argument(
        "-type",
        help=(
            """
            Select web search or host search(default host) 
            """
        ),
        choices={'web', 'host'},
        default="host"
    )
    parser_search.add_argument(
        "-force",
        help=(
            """
            Ignore the local cache and force the data to be obtained from the API
            """
        ),
        action="store_true"
    )
    parser_search.set_defaults(func=core.search)

    # initial account configuration related commands
    parser_init = subparsers.add_parser("init", help="Initialize the token for ZoomEye-python")
    parser_init.add_argument("-apikey", help="ZoomEye API Key", default=None, metavar='[api key]')
    parser_init.add_argument("-username", help="ZoomEye account username", default=None, metavar='[username]')
    parser_init.add_argument("-password", help="ZoomEye account password", default=None, metavar='[password]')
    parser_init.set_defaults(func=core.init)

    parser_ip_info = subparsers.add_parser("ip", help="Query IP information")
    parser_ip_info.add_argument("ip", help="search device IP", metavar='ip', type=str)
    parser_ip_info.add_argument(
        "-filter",
        help="output more clearer search results by set filter field,field:[port,service,app,banner]",
        default=None,
        metavar="key=value")
    parser_ip_info.set_defaults(func=core.information_ip)

    # query ip history
    parser_history = subparsers.add_parser("history", help="Query device history")
    parser_history.add_argument("ip", help="search historical device IP", metavar='ip', type=str)
    parser_history.add_argument(
        "-filter",
        help=("""
            filter data and print raw data detail.
            field: [timestamp,port,service,country,banner,*]
        """),
        metavar='filed=regexp',
        type=str,
        default=None,
        const="app",
        nargs='?'
    )
    parser_history.add_argument(
        "-force",
        help=(
            """
            ignore the local cache and force the data to be obtained from the API
            """
        ),
        action="store_true"
    )
    parser_history.add_argument(
        '-num',
        help='The number of search results that should be returned',
        type=int,
        default=None,
        metavar='value'
    )
    parser_history.set_defaults(func=core.ip_history)

    parser_clear = subparsers.add_parser("clear", help="Manually clear the cache and user information")
    parser_clear.add_argument(
        "-setting",
        help="clear user api key and access token",
        action="store_true"
    )
    parser_clear.add_argument(
        "-cache",
        help="clear local cache file",
        action="store_true"
    )
    parser_clear.set_defaults(func=core.clear_file)

    args = parser.parse_args()

    if args.version:
        get_version()
        exit(0)

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
