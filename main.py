from terminalInterface import CLI
from InMemStore import PyInMemStore


db = PyInMemStore()
cli = CLI(db)

print("SET       <key> <value>")
print("GET       <key>")
print("DELETE    <key>")
print("EXPIRE    <key> <seconds>")
print("TTL       <key>")
print("LSET     <key> <item-1> <item-2> ... <item-n>")
print("LPOP      <key>")
print("COMMIT")
print("ROLLBACK")
print("\n   ---All commands are case insensitive---")
print("-"*84)

cli.start()