"""
Centralized logging configuration for CarCompare.

build_logging_config() is a factory function rather than a module-level
dict because LOGGING depends on BASE_DIR, which lives in base.py. Keeping
this file free of that dependency means it has zero knowledge of where
it's used — it only needs a Path object passed in, making it portable
to other projects without modification.
"""

def build_logging_config(base_dir):
    """
    Build the LOGGING dict for Django.

    Args:
        base_dir: Path object pointing to the project root, used to
                   construct the path to the logs directory.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        
        
        "formatters": {
            "verbose": {
                # Example: WARNING 2026-06-20 14:32:01 car_view 8842 Variant not found
                "format": "{levelname} | {asctime} | {module}:{lineno} | PID:{process:d} | {message}",
                "style": "{",
            },
            "simple": {
                # Example: INFO | 2026-06-20 14:32:01 | Variant viewed
                "format": "{levelname} | {asctime} | {message}",
                "style": "{",
            }
        },
        
        
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "production_file": {
                "level": "WARNING",
                "filters": ["require_debug_false"],
                "class": "logging.handlers.RotatingFileHandler",
                "filename": base_dir / "logs" / "django.log",
                "maxBytes": 1024*1024*10, # 10MB then rotate
                "backupCount": 5, # Only save 5 lastest logging files
                "formatter": "verbose",  
            },
            "mail_admin": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
                "formatter": "verbose",
            },
        },
        
        "loggers": {
            "django": {
                "handlers": ["console", "production_file"],
                "level": "INFO",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["mail_admin", "production_file"],
                "level": "ERROR",
                "propagate": False,
            },
            "cars": {
                "handlers": ["mail_admin", "production_file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "api": {
                "handlers": ["mail_admin", "production_file"],
                "level": "DEBUG",
                "propagate": False,
            }
        }
    }