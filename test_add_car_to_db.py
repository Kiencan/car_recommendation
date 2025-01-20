import json
from personalization_models import ProductRequest, ContentRequest
from personalization import add_product_to_qdrant, add_content_to_qdrant
from personalization import create_qdrant_collection_if_not_exists, PRODUCT_VECTOR_SIZE, CONTENT_VECTOR_SIZE


def process_and_save_car_data(json_file_path):
    # Tạo collection cdp_product và cdp_content nếu chưa tồn tại
    create_qdrant_collection_if_not_exists("cdp_product", PRODUCT_VECTOR_SIZE)
    create_qdrant_collection_if_not_exists("cdp_content", CONTENT_VECTOR_SIZE)

    # Load the car data from the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        car_datas = json.load(file)

    # Extract the common fields from car data
    for car_data in car_datas: 
        car_id = car_data["ma_xe"] if car_data["ma_xe"] else None
        car_name = car_data["ten_xe"]
        car_brand = car_data["hang_xe"] if car_data["hang_xe"] else None
        car_price = car_data["gia"] if car_data["gia"] else None
        car_location = car_data["dia_diem_ban"] if car_data["dia_diem_ban"] else None
        car_image = car_data["link_anh"] if car_data["link_anh"] else ""
        car_year = car_data["nam_san_xuat"] if car_data["nam_san_xuat"] else None
        car_condition = car_data["tinh_trang"] if car_data["tinh_trang"] else None
        car_keywords = [
            car_data["hang_xe"] if car_data["hang_xe"] else None,
            car_data["kieu_dang"] if car_data["kieu_dang"] else None,
            car_data["nhien_lieu"] if car_data["nhien_lieu"] else None,
            car_data["hop_so"] if car_data["hop_so"] else None,
            car_data["mau_ngoai_that"] if car_data["mau_ngoai_that"] else None,
            car_data["xuat_xu"] if car_data["xuat_xu"] else None,
            str(car_data["nam_san_xuat"] if car_data["nam_san_xuat"] else None)
        ]

        # Prepare additional info for product and content
        additional_info = {
            "price": car_price,
            "location": car_location,
            "image": car_image,
            "condition": car_condition,
            "year": car_year,
            "mileage": car_data["so_km_da_di"] if car_data["so_km_da_di"] else None,
            "seats": car_data["so_cho_ngoi"] if car_data["so_cho_ngoi"] else None,
            "doors": car_data["so_cua"] if car_data["so_cua"] else None,
            "drive": car_data["dan_dong"] if car_data["dan_dong"] else None,
            "engine_capacity": car_data["dung_tich_dong_co"] if car_data["dung_tich_dong_co"] else None
        }
        print(car_image)
        # Create and save ProductRequest
        product_request = ProductRequest(
            product_id=car_id,
            product_name=car_name,
            product_category=car_brand,
            product_keywords=car_keywords,
            url=car_image,
            additional_info=additional_info,
            journey_maps=[]
        )
        add_product_to_qdrant(product_request)

        # Create and save ContentRequest
        content_request = ContentRequest(
            content_id=car_id,
            title=car_name,
            description=f"Xe {car_name}, tình trạng: {car_condition}, giá: {car_price} tại {car_location}",
            content="",  # No detailed content provided in the input
            content_type="car",
            url=car_image,
            content_category=car_brand,
            content_keywords=car_keywords,
            additional_info=additional_info,
            journey_maps=[]
        )
        add_content_to_qdrant(content_request)

        print(f"Car data with ID {car_id} has been saved to both collections.")


# Example usage:
process_and_save_car_data("transformed_car_data.json")
