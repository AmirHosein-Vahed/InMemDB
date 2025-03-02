## In Memory Database Project

### Like Redis but in python :)


This DB has below operations:

| COMMAND | ATTRIBUTES |
|---------|------------|
|SET      | [key] [value] |
|GET      | [key] |
|DELETE   | [key] |
|EXPIRE   | [key] [seconds] |
|TTL      | [key] |
|LSET     | [key] [item-1] [item-2] ... [item-n] |
|LPOP     | [key] |
|COMMIT   | --- |
|ROLLBACK | --- |
