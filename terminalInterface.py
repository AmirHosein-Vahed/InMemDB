from InMemStore import PyInMemStore
from Validation import Validation

class CLI:
    def __init__(self, db: PyInMemStore):
        self.db = db

    def start(self):
        validate = Validation()
        while True:
            input_command = input().split(" ")
            match str(input_command[0]).upper():
                case "SET":
                    if validate.set_command(input_command):
                        self.db.set(input_command[1], input_command[2])

                case "GET":
                    if validate.get_command(input_command):
                        print(self.db.get(input_command[1]))

                case "DELETE":
                    if validate.delete_command(input_command):
                        self.db.delete(input_command[1])

                case "EXPIRE":
                    if validate.expire_command(input_command):
                        self.db.expire(input_command[1], float(input_command[2]))

                case "TTL":
                    if validate.ttl_command(input_command):
                        self.db.ttl(input_command[1])

                case "COMMIT":
                    if validate.commit_command(input_command):
                        self.db.commit()

                case "ROLLBACK":
                    if validate.rollback_command(input_command):
                        self.db.rollback()

                case "LSET":
                    if validate.lpush_command(input_command):
                        self.db.lpush(input_command[1], input_command[2:])

                case "LPOP":
                    if validate.lpop_command(input_command):
                        self.db.rpop(input_command[1])

                case _:
                    print("Command Not Found.")
                