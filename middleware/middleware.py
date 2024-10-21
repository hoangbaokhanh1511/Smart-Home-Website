import functools
from flask import session,redirect

def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if 'username' not in session and 'id' not in session:
            return redirect('/login')
        return view_func(*args, **kwargs)
    return decorated