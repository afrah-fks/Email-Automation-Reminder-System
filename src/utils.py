def load_template(path):
    with open(path, "r") as file:
        return file.read()

def personalize_message(template, name):
    return template.replace("{name}", name)