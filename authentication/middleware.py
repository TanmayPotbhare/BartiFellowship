import functools
from flask import session, redirect

# Middle Ware Authentication
def auth(view_fun):
    @functools.wraps(view_fun)
    def decorated(*args, **kwargs):
        if 'email' not in session:
            return redirect('/login')
        return view_fun(*args, **kwargs)
    return decorated

def auth_admin(view_fun):
    @functools.wraps(view_fun)
    def decorated(*args, **kwargs):
        if 'email' not in session:
            return redirect('/adminlogin')
        return view_fun(*args, **kwargs)
    return decorated