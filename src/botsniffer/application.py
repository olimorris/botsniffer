import re
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from botsniffer import __version__
from botsniffer.counter import Counter
from botsniffer.formatter import Formatter
from botsniffer.search import Search
from botsniffer.tree import Tree

app = typer.Typer(add_completion=False)
default_depth = 10
output_string = "\n-------------- OUTPUT ---------------"


def version_callback(value: bool):
    if value:
        typer.echo(f"BotSniffer Version: {__version__}")
        raise typer.Exit()


def get_search_dir(bot: str):
    match = re.search(r".*Automation Anywhere/Bots/", bot)

    if match:
        search_dir = match.group(0)
        return search_dir

    return ""


@app.command()
def main(
    bot: Annotated[
        str,
        typer.Option(
            help="The path of the bot to search. This is typically referred to as the 'parent' bot",
        ),
    ] = "",
    search_dir: Annotated[
        Optional[str],
        typer.Option(
            help="(Optional) The path of the directory to search for nested bots",
        ),
    ] = "",
    cr_path: Annotated[
        Optional[str],
        typer.Option(
            help="(Optional) The file path to the Control Room directory",
        ),
    ] = "repository:///Automation Anywhere/Bots/",
    depth: Annotated[
        Optional[int],
        typer.Option(
            help="The depth of the tree to display",
        ),
    ] = default_depth,
    save: Annotated[
        Optional[bool],
        typer.Option(
            help="Save the output to a file",
        ),
    ] = False,
    summarize: Annotated[
        bool,
        typer.Option(
            help="Output the amount of times a bot is called in the parent bot",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            help="Show the version and exit.",
        ),
    ] = None,
):
    """
    Sniff out the structure of a bot and its dependencies
    """
    if not bot:
        print("[bold red]Error:[/bold red] Please provide a path to the bot")
        print("See 'botsniffer --help' for more information.")
        raise typer.Exit(code=1)

    if not search_dir:
        search_dir = get_search_dir(bot)
        print(
            f"[bold blue]Info:[/bold blue] Using [italic]{search_dir}[/italic] as the search directory"
        )

    search = Search(search_dir, cr_path)

    # Make the parent bot the first item in the dictionary
    bot_name = bot.replace(search_dir, "")
    search.within_bot(bot, bot_name)

    # Search the parent for nested bots
    if bot_name in search.bot_output:
        for bot in search.bot_output[bot_name]:
            if bot not in search.searched_bots:
                search.within_bot(search_dir + bot, bot)

    # Search the nested bots for more nested bots
    for bot_key in list(search.bot_output.keys()):
        for bot in search.bot_output[bot_key]:
            if bot not in search.searched_bots:
                search.within_bot(search_dir + bot, bot.replace(search_dir, ""))

    if search.bot_output:
        if summarize:
            counter = Counter(search.bot_output).count()

            if save:
                counter.save2file("bot_count.json")
                return print(
                    "\n[bold green]Success![/bold green] Output saved to bot_count.json"
                )

            sorted = counter.sort()

            print(output_string)
            print(sorted)
            return

        tree = Tree(search.bot_output).grow(bot_name)
        formatted_tree = Formatter(tree).to_tree(bot_name)

        if depth != default_depth:
            formatted_tree.prune(depth)

        if save:
            output = formatted_tree.tree.to_json(sort=False)
            with open("bot_tree.json", "w") as file:
                file.write(output)

            return print(
                "\n[bold green]Success![/bold green] Output saved to bot_tree.txt"
            )

        print(output_string)
        return formatted_tree.tree.show(sorting=False)
    else:
        print("[bold blue]Info:[/bold blue] Could not find any dependencies")


if __name__ == "__main__":
    app()
