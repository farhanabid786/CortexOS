from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.core.config import settings
import logging

logger = logging.getLogger("cortexos-db")

# Determine if we are using SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

if is_sqlite:
    logger.warning(
        "\n================================================================================\n"
        "WARNING: CortexOS is currently running with a local SQLite database.\n"
        "If you are deploying this application on a platform with ephemeral storage\n"
        "(such as Render, Heroku, Railway, or Fly.io), your data WILL be lost whenever\n"
        "the server restarts or goes to sleep.\n\n"
        "To persist your data, either:\n"
        "1. Attach a Persistent Disk volume and point your DATABASE_URL to it\n"
        "   (e.g., sqlite+aiosqlite:////data/cortexos.db)\n"
        "2. Configure an external PostgreSQL database and set the DATABASE_URL env var\n"
        "   (e.g., postgresql+asyncpg://user:pass@host:port/dbname)\n"
        "================================================================================"
    )

# SQLAlchemy base class
Base = declarative_base()

# Configure engine arguments
connect_args = {}
if is_sqlite:
    # SQLite requires separate thread configuration for safety, though custom write locks are handled by aiosqlite
    connect_args["check_same_thread"] = False

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

# Async Session Factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Enforce foreign key constraints in SQLite
if is_sqlite:
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Dependency to get async db session
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
