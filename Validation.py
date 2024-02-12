class Validation:
    def __init__(self):
        ...

    def _has_length(self, _list: list, length: int) -> bool:
        return len(_list) == length

    def set_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 3):
            print_exception("Usage", "SET <key> <value>")
            return False
        return True

    def get_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 2):
            print_exception("Usage", "GET <key>")
            return False
        return True

    def delete_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 2):
            print_exception("Usage", "DELETE <key>")
            return False
        return True

    def expire_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 3):
            print_exception("Usage", "EXPIRE <key> <seconds>")
            return False
        return True

    def ttl_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 2):
            print_exception("Usage", "TTL <key>")
            return False
        return True

    def commit_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 1):
            print_exception("Usage", "COMMIT")
            return False
        return True

    def rollback_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 1):
            print_exception("Usage", "ROLBACK")
            return False
        return True

    def lpush_command(self, input_command: list) -> bool:
        if len(input_command) <= 2:
            print_exception("Usage", "LSET <key> <item-1> <item-2> ... <item-n>")
            return False
        return True

    def lpop_command(self, input_command: list) -> bool:
        if not self._has_length(input_command, 2):
            print_exception("Usage", "LPOP <key>")
            return False
        return True


def print_exception(title: str, msg: str):
    print(f"{title} Error: {msg}")