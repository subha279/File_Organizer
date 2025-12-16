_undo_stack = []


def add_undo(src, dest):
    _undo_stack.append((src, dest))


def undo_all():
    import os
    import shutil

    for src, dest in reversed(_undo_stack):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(src, dest)
    _undo_stack.clear()
