"""WSGI entry point for production servers such as Gunicorn or Waitress."""

from app import create_app

app = create_app()
