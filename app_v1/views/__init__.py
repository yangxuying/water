from flask import session


def is_admin():
    return session.get('role') == "管理员"
