import dj_database_url

from .env import config

# Fetch the DATABASE_URL from the environment variables.
# If it's not set, default to None.
DATABASE_URL = config("DATABASE_URL", default=None)

# If DATABASE_URL is set, configure the Django database settings.
# Use dj_database_url to parse the DATABASE_URL and set up the database connection.
# Set the maximum age of database connections to 600 seconds.
# Enable connection health checks.
if DATABASE_URL is not None:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL, conn_max_age=600, conn_health_checks=True
        )
    }
