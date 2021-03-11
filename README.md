pre-commit hook to remove cell output of .ipynb notebook and some metadata for better security.

Sample config:
```
repos:
  - repo: https://github.com/roy-ht/pre-commit-jupyter
    rev: v1.2.0
    hooks:
      - id: jupyter-notebook-cleanup
        args:
          - --remove-kernel-metadata
          - --pin-patterns
          - "[pin];[donotremove]"
```

If you have "pin patterns", You can keep cell outputs like that:

```
# [pin]
some_function()
print("some info")
```

```
# [donotremove]
some_function()
print("some info")
```
