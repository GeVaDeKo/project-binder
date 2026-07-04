# Project Binder

Automatically generate an AI-friendly overview of your Laravel project (and Python later on).

## Install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/GeVaDeKo/project-binder/main/install.sh)
```

## Update
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/GeVaDeKo/project-binder/main/update.sh)
```

## Usage

```bash
binder ~/path/to/your/project
```

if you want to focus to a specific i.e. User controller/model/service/view/routes use:
```bash
binder ~/path/to/your/project --focus User
```
This will also find controllers such as "RegisteredUserController", and other models that use the User model.

Focus can be used with other flags such as:
```bash
-d -c -m -v -s -r
```
-d: Will only include database information.<br>
-c: Will only include controllers.<br>
-m: Will only include models.<br>
-v: Will only include views.<br>
-s: Will only include services.<br>
-r: Will only include route information.<br>

So
```bash
binder ~/path/to/your/project --focus User -c -m
```
Will only return controllers with "User" in the name, the "User" model and all models that use the "User" model.
