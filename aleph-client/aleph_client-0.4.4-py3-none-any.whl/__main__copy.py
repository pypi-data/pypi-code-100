@app.command()
def get():
    try:
        messages = sync_get_messages()
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Chain")
        table.add_column("Type")
        table.add_column("Channel")
        table.add_column("item_type")
        table.add_column("Size")
        table.add_column("Time")
        for message in messages["messages"][:10]:
            table.add_row(
                message["chain"],
                message["type"],
                message["channel"],
                message["item_type"],
                str(message["size"]),
                str(message["time"]),
            )
        console.print(table)
    finally:
        # Prevent aiohttp unclosed connector warning
        asyncio.get_event_loop().run_until_complete(get_fallback_session().close())
