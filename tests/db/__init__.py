from typing import Generator
from faker import Faker
from sqlalchemy import func
from app import db
from app import models as m


faker = Faker()

NUM_TEST_USERS = 100


def gen_test_items(num_objects: int) -> Generator[str, None, None]:
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    i = db.session.query(func.max(m.User.id)).scalar()

    for _ in range(num_objects):
        i += 1
        # Primary name
        first_name = fake.first_name()

        # Secondary name
        last_name = fake.last_name()

        company = fake.company().split()[0].strip(",")

        # Company DNS
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]

        # email formatting
        yield f"{first_name}{i}".lower(), f"{first_name}.{last_name}{i}@{company}.{dns_org}".lower()


def populate(count: int = NUM_TEST_USERS):
    for username, email in gen_test_items(count):
        m.User(
            username=username,
            email=email,
        ).save(False)

    db.session.commit()
