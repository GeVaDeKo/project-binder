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
A "_project_context.json" file will be automatically be created when you use "--focus".<br>
<div style="display: flex; justify-content: center; margin-top:6px; width: 100%;">
  <img style="width: 32%; padding-top:6px;" alt="project_context" src="https://github.com/user-attachments/assets/23265b26-f59f-4138-9be2-8362ade4b436" />
  <img style="width: 32%; padding-top:6px;" alt="user_context" src="https://github.com/user-attachments/assets/bc1a7a3d-3e83-4b71-b2eb-f272415ef39c" />
  <img style="width: 32%; padding-top:6px;" alt="tree_structure" src="https://github.com/user-attachments/assets/dea62278-f195-4013-8d5c-a890bcde0862" />
</div>