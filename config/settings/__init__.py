# Making sure we run dev settings only if they are available i.e if we are not
# in a production environment

try:
    from .development import *
except:
    from .production import *
