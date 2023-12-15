import json


class Search:
    """
    Iteratively search through a bot
    """

    def __init__(self, search_dir, cr_path):
        self.search_dir = search_dir
        self.cr_path = cr_path

        self.bot_output = {}
        self.searched_bots = []

    def within_bot(self, bot, key):
        """
        Search the bot for nested bots
        """
        try:
            with open(bot, "r", encoding="utf-8") as file:
                if key:
                    self.bot_output[key] = []

                json_data = json.load(file)
                self.get_bots_recursively(json_data, self.search_dir, key)
                self.searched_bots.append(bot.replace(self.search_dir, ""))

                return
        except Exception as e:
            print(f"Error reading or processing file {bot}: {e}")
            return None

    def get_bots_recursively(self, node, search_dir, key=None):
        if isinstance(node, list):
            for item in node:
                self.get_bots_recursively(item, search_dir, key)

        elif isinstance(node, dict):
            # Exclude commented out commands
            if node.get("disabled") is True:
                return

            if node.get("commandName") == "runTask":
                taskbot_file = (
                    node.get("attributes", [{}])[0]
                    .get("value", {})
                    .get("taskbotFile", {})
                )
                if taskbot_file.get("type") == "FILE":
                    bot = (
                        taskbot_file.get("string")
                        .replace("%20", " ")
                        .replace(self.cr_path, "")
                    )
                    self.bot_output[key].append(bot)

            # Recursively search in any nested nodes or children
            for _, value in node.items():
                if isinstance(value, (dict, list)):
                    self.get_bots_recursively(value, search_dir, key)
