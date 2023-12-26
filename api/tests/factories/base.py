from faker.providers import BaseProvider


class PhoneNumberProvider(BaseProvider):
    def fake_phone_number(self) -> str:
        return f"{self.generator.phone_number()}"[:20]
