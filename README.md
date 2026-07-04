# Project Binder

Automatically generate an AI-friendly overview of your Laravel project (and Python later on).

## Install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/GeVaDeKo/project-binder/main/install.sh)
```

## Update
Maybe there is an update (you never know) use:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/GeVaDeKo/project-binder/main/update.sh)
```
to update 😁

## Usage

```bash
binder ~/path/to/your/project
```

if you want to focus to a specific i.e. User controller/model/service/view/routes use:
```bash
binder ~/path/to/your/project --focus User
```
This will also find usages such as "UserUpload".

Focus can be used with other flags such as:
```bash
-d -c -m -v -s
```
-d: Will only include database information.<br>
-c: Will only include controllers.<br>
-m: Will only include models.<br>
-v: Will only include views.<br>
-s: Will only include services.<br>

So
```bash
binder ~/path/to/your/project --focus User -c -m
```
Will only return models and controllers with "User" in the name.
