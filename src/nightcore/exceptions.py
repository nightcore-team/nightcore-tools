"""Custom exceptions for the Nightcore application."""


class CommandDontHavePermissionsFlagError(Exception):
    def __init__(self, command_name: str):
        self.command_name = command_name
        super().__init__(f"{command_name}")
