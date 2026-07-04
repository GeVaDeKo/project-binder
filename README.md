# Project Binder

Generate structured project context that helps AI understand your codebase.

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

To generate context for a specific feature (for example: User):
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
Returns controllers matching "User", the User model, and related models that reference the User model.<br>
<img width="306" height="271" alt="image" src="https://github.com/user-attachments/assets/8257dde1-60d0-4ead-9632-6c0b1afbac88" />
<img width="423" height="339" alt="image" src="https://github.com/user-attachments/assets/3e8685ef-5480-44e0-8cb4-8bbd118e7096" />
