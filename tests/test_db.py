from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='everson',
        email='everson@esteves.com',
        password='123@',
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'everson@esteves.com')
    )

    assert result.id == 1
