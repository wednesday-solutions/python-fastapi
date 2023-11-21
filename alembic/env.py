import json
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

load_dotenv()

print("==" * 50, "\n\n\n", "OS ENVIRONMENT", os.environ, "\n\n\n", "==" * 50)

if "PYTHON_FASTAPI_TEMPLATE_CLUSTER_SECRET" in os.environ:
    print("Connecting to database on RDS..\n")
    dbSecretJSON = os.environ["PYTHON_FASTAPI_TEMPLATE_CLUSTER_SECRET"]
    dbSecretParsed = json.loads(dbSecretJSON)

    HOST = dbSecretParsed["host"]
    PORT = dbSecretParsed["port"]
    DBNAME = dbSecretParsed["dbname"]
    USERNAME = dbSecretParsed["username"]
    PASSWORD = dbSecretParsed["password"]

else:
    print("Connecting local database..\n")
    HOST = os.environ["DB_HOSTNAME"]
    PORT = os.environ["DB_PORT"]
    DBNAME = os.environ["DB_NAME"]
    USERNAME = os.environ["DB_USERNAME"]
    PASSWORD = os.environ["DB_PASSWORD"]

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# here we allow ourselves to pass interpolation vars to alembic.ini
# fron the host env
section = config.config_ini_section

config.set_section_option(section, "DB_USER", USERNAME)
config.set_section_option(section, "DB_PASS", PASSWORD)
config.set_section_option(section, "DB_HOST", HOST)
config.set_section_option(section, "DB_PORT", str(PORT))
config.set_section_option(section, "DB_NAME", DBNAME)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()