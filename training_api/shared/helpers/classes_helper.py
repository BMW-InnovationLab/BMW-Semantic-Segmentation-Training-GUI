def get_num_classes(classes_path: str) -> int:
    classes: str = open(classes_path, 'r').read()
    return len(classes.split(','))
