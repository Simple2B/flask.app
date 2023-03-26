from typing import Generator
from app import db
from app import models as m
from faker import Faker


faker = Faker()


def gen_test_items(num_objects: int) -> Generator[str, None, None]:
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    for _ in range(num_objects):
        # Primary name
        first_name = fake.first_name()

        # Secondary name
        last_name = fake.last_name()

        company = fake.company().split()[0].strip(",")

        # Company DNS
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]

        # email formatting
        yield first_name, f"{first_name}.{last_name}@{company}.{dns_org}".lower()


def populate():
    NUM_TEST_USERS = 100
    for index, object in enumerate(gen_test_items(NUM_TEST_USERS)):
        m.User(
            username=object[0] + str(index),
            email=object[1],
            password="password",
        ).save(False)
    db.session.commit()
