# Variable Arugments

- You can define variables using the `-v "variable_name=variable_value"` argument
- You may use multiple `-v` arguments
- One variable per `-v` argument, where the variable name (key) to the left of a `=`, with the value of the variable to the right of the `=`.
- Lists can be used as values by separating list items with the two characters `\,`
  - For example: `-v "my_list=item 1\,item 2\,item 3\,"`
  - Which turns into a python list object equivalent to `{my_list: ["item 1", "item 2", "item 3"]}`