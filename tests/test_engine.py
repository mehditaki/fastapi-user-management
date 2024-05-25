import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


@pytest.fixture(scope="session")
def test_engine():
    """test_engine.

    Scope: session

    Description: Provides a SQLAlchemy engine instance for testing purposes.

    """
    engine = create_engine("sqlite:///:memory:")
    declarative_base()
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Scope: function.

    Description: Provides a SQLAlchemy session object for testing database interactions within a test function.

    Parameters:
    test_engine: A fixture providing a SQLAlchemy engine instance.
    """
    connection = test_engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_database_connection(test_session):
    """Description: Tests the functionality of the database connection.

    Parameters:
        test_session: A fixture providing a session object for interacting with the database.

    Returns: None.

    """
    result = test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
