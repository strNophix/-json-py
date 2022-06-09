# json-py

Simple JSON-parser written in python.

Inspired by [Phil Eaton's article](https://notes.eatonphil.com/writing-a-simple-json-parser.html).

## Example usage
```python
import json_py
print(json_py.from_json('{"hello": ["world", "!", 69], 3: 9.1}'))
# {'hello': ['world', '!', 69], 3: 9.1}
```

## Todo
Implement `json_py.to_json()`