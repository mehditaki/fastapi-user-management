try:
    from importlib_metadata import version
    __version__ = version(__name__)
except Exception:
    __version__ = "0.1.0"