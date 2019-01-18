# `Conan CLion Workspace Generator`
TODO...

## Usage
Add conan repository:
```
$ conan remote add adigie https://api.bintray.com/conan/adigie-conan/conan 
```

Use package in conan recipe:
```python
from conans import ConanFile, python_requires

ccwg = python_requires("conan-clion-workspace-generator/0.1.0@adigie/testing")

class Conan(ConanFile):
    ...
    def build(self):
        ...
        cg = ccwg.ClionWorkspaceGenerator(self)
        cg.generate()
        ...
    ...
```