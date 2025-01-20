from faker import Faker
from personalization_models import ProfileRequest
from personalization import add_profile_to_qdrant, create_qdrant_collection_if_not_exists, PROFILE_VECTOR_SIZE
import random

# Tạo dữ liệu giả
fake = Faker()

def generate_random_keywords():
    car_brands = ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Mitsubishi"]
    car_types = ["SUV", "Sedan", "Hatchback", "Convertible", "Truck"]
    actions = ["buy", "sell", "review", "compare", "test drive"]

    return [
        f"{random.choice(actions)} {random.choice(car_brands)} {random.choice(car_types)}"
        for _ in range(random.randint(3, 5))
    ]

def create_fake_profiles(num_profiles=100):
    # Tạo collection cdp_profile nếu chưa tồn tại
    create_qdrant_collection_if_not_exists("cdp_profile", PROFILE_VECTOR_SIZE)

    for _ in range(num_profiles):
        profile_id = fake.uuid4()
        page_view_keywords = generate_random_keywords()
        purchase_keywords = generate_random_keywords()
        interest_keywords = generate_random_keywords()

        profile_request = ProfileRequest(
            profile_id=profile_id,
            page_view_keywords=page_view_keywords,
            purchase_keywords=purchase_keywords,
            interest_keywords=interest_keywords,
            additional_info={
                "name": fake.name(),
                "email": fake.email(),
                "location": fake.city(),
                "age": random.randint(18, 70)
            }
        )

        # Lưu thông tin vào Qdrant
        add_profile_to_qdrant(profile_request)

    print(f"Generated and saved {num_profiles} fake profiles to Qdrant.")

# Gọi hàm tạo dữ liệu giả
create_fake_profiles(100)
