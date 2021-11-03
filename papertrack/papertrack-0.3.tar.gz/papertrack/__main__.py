
from ast import Param
from papertrack.core.Loggable import Loggable
from papertrack .simple import * 
from papertrack.core import * 
import argparse
from papertrack.curses import curses_ask_fn

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="group")
    get_group = subparsers.add_parser("get")
    view_group = subparsers.add_parser("view")

    for group_name in ["collector", "downloader", "viewer"]:
        group = subparsers.add_parser(group_name)
        group.add_argument("--list", action="store_true", help="List all instances that can be used for %s" % group_name)
        group.add_argument("--describe", metavar=group_name, help="Show available options for particular %s" % group_name)

    get_group.add_argument("--downloader", choices=list(downloader.name for downloader in get_all_components("downloader")))
    get_group.add_argument("--collector", choices=list(collector.name for collector in get_all_components("collector")))

    view_group.add_argument(
        "--viewer", 
        choices=list(x.name for x in get_all_components("viewer")), 
        default="simple" if "simple" in [y.name for y in get_all_components("viewer")] else get_all_components("viewer")[0].name
    )

    args, rest = parser.parse_known_args()

    def get_component_parser(name, type):
        component = get_component_class(name, type)
        parser = argparse.ArgumentParser(prog=f"papertrack ... --{type} {component.name}")
        for param, definition in component.params.items():
            additional_config = {}
            if definition["type"] == "list":
                additional_config = {
                    "action": "extend",
                    "nargs": "+"
                }
            arg_name = "--download-%s" % param if type == "downloader" else "--%s" % param
            parser.add_argument(
                arg_name, 
                help=definition.get("description", "") + " (Default: " + definition.get("default", "none") + ")", 
                choices=definition.get("choices", None), 
                **additional_config
            )

        return parser

    ask_fn = None
    if os.environ.get("PAPERTRACK_ASK_FN", "curses") == "curses":
        ask_fn = curses_ask_fn
    elif os.environ.get("PAPERTRACK_ASK_FN", "curses") == "cli":
        ask_fn = simple_ask_fn
    else:
        print("Wrong value for PAPERTRACK_ASK_FN")
        exit(2)

    if args.group == "get":
        downloader_parser = get_component_parser(args.downloader, type="downloader")
        collector_parser = get_component_parser(args.collector, type = "collector")

        downloader_args, rest = downloader_parser.parse_known_args(rest)
        collector_args = collector_parser.parse_args(rest)
        downloader_config = {param: getattr(downloader_args, "download_%s" % param) for param in get_component_class(
            args.downloader, 
            "downloader"
        ).params.keys() if hasattr(downloader_args, "download_%s" % param)}

        collector_config = {param: getattr(collector_args, "%s" % param) for param in get_component_class(
            args.collector, 
            "collector"
        ).params.keys() if hasattr(collector_args, "%s" % param)}


        downloader_config = {k:v for k,v in downloader_config.items() if v is not None}
        collector_config = {k:v for k,v in collector_config.items() if v is not None}

        downloader = get_downloader_instance(args.downloader, ask_fn, **downloader_config)
        collector = get_collector_instance(args.collector, ask_fn, **collector_config)
        os.makedirs(os.path.join(os.environ["HOME"], ".papertrack"), exist_ok=True)
        journal_location = os.path.join(os.environ["HOME"], ".papertrack", "journal.json")
        downloader = Loggable(downloader, journal_location)
        collector = Loggable(collector, journal_location)

        location = downloader.download()
        db = Database()
        entry = collector.collect(location)
        db.save(entry)

    elif args.group == "view":
        viewer_parser = get_component_parser(args.viewer, type="viewer")
        viewer_args, rest = viewer_parser.parse_known_args(rest)
        viewer_config = {param: getattr(viewer_args, "%s" % param) for param in get_component_class(
            args.viewer, 
            "viewer"
        ).params.keys() if hasattr(viewer_args, "%s" % param)}
        viewer_config = {k:v for k,v in viewer_config.items() if v is not None}
        viewer = get_viewer_instance(args.viewer, ask_fn, **viewer_config)
        db = Database()
        viewer.view(db.list())
    else:
        if args.list:
            for item in get_all_components(args.group):
                print(item.name)
            exit(0)
        if args.describe is not None:
            get_component_parser(args.describe, args.group).print_help()
if __name__ == "__main__":
    main()