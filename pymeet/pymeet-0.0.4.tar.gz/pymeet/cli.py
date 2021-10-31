import click

import pymeet


@click.group()
def main(): ...


@main.command()
def start():
    app = pymeet.PyMeet((1080, 720), 30)
    app.start()


@main.command()
@click.argument('text')
@click.option('--option', is_flag=True)
def echo(text, option):
    option_text = ' (option added)' if option else ''
    click.echo(text + option_text)


main.add_command(start, 'start')
main.add_command(echo, 'echo')


if __name__ == '__main__':
    main()
