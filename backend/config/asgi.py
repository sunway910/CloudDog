"""
ASGI config for backend project.

It exposes the ASGI(Python Async Server Gateway Interface) callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# ASGI(Python Async Server Gateway Interface)是WSGI的精神继承者，WSGI是用于Web服务器、框架和应用程序之间兼容性的长期存在的Python标准
#
# WSGI成功地在Python网络空间中提供了更多的自由和创新，而ASGI的目标是将这一点继续推进到异步Python的领域
#
# ASGI is a spiritual successor to WSGI, the long-standing Python standard for compatibility between web servers, frameworks, and applications.
#
# WSGI succeeded in allowing much more freedom and innovation in the Python web space, and ASGI’s goal is to continue this onward into the land of asynchronous Python.


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
