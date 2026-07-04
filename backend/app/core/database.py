from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.core.config import settings

# Determine if we are using SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

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
