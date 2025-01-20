from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from personalization import build_product_vector
from personalization import qdrant_client, PRODUCT_COLLECTION
from qdrant_client.http.models import Filter, FieldCondition, MatchAny
from typing import Optional

app = FastAPI()

class UserInput(BaseModel):
    seats: Optional[int] = ""
    color: Optional[str] = ""
    condition: Optional[str] = ""
    brand: Optional[str] = ""
    year: Optional[int] = ""
    keywords: Optional[str] = ""

def recommend_cars(user_input: dict, top_n=5):
    """
    Gợi ý xe dựa trên thông tin người dùng nhập vào.

    :param user_input: dict chứa các thông tin tìm kiếm như số chỗ, màu ngoại thất, tình trạng, hãng xe, năm sản xuất, ...
    :param top_n: Số lượng xe gợi ý (mặc định là 5)
    :return: Danh sách các xe được gợi ý
    """
    # Tạo danh sách bộ lọc dựa trên đầu vào
    must_filter = []

    if "seats" in user_input:
        must_filter.append(FieldCondition(key="additional_info.seats", match=MatchAny(any=[user_input["seats"] if user_input["seats"] else ""])))

    if "color" in user_input:
        must_filter.append(FieldCondition(key="additional_info.color", match=MatchAny(any=[user_input["color"] if user_input["color"] else ""])))

    if "condition" in user_input:
        must_filter.append(FieldCondition(key="additional_info.condition", match=MatchAny(any=[user_input["condition"] if user_input["condition"] else ""])))

    if "brand" in user_input:
        must_filter.append(FieldCondition(key="keywords", match=MatchAny(any=[user_input["brand"] if user_input["brand"] else ""])))

    if "year" in user_input:
        must_filter.append(FieldCondition(key="additional_info.year", match=MatchAny(any=[user_input["year"] if user_input["year"] else ""])))

    # Tạo vector tìm kiếm nếu có từ khóa hợp lệ
    search_vector = None
    if "keywords" in user_input and user_input["keywords"]:
        user_input["keywords"] = user_input["keywords"].split(" ")
        non_empty_keywords = [kw for kw in user_input["keywords"] if kw.strip()]
        if non_empty_keywords:
            search_vector = build_product_vector(
                product_name=" ".join(non_empty_keywords),
                product_category="car",
                product_keywords=non_empty_keywords,
                journey_maps=[]
            )
    else:
        p_name = ""
        for key, value in user_input.items():
            if isinstance(value, int):
                p_name = p_name + str(value) + " "
            else:
                p_name = p_name + value + " "

        search_vector = build_product_vector(
            product_name=p_name,
            product_category="car",
            product_keywords=user_input,
            journey_maps=[]
        )
    try:
        # Tìm kiếm sản phẩm trong Qdrant
        search_results = qdrant_client.search(
            collection_name=PRODUCT_COLLECTION,
            query_vector=search_vector if search_vector is not None else None,
            query_filter=Filter(should=must_filter) if must_filter else None,
            limit=top_n
        )
        # print(search_results)
        # Trích xuất thông tin sản phẩm từ kết quả tìm kiếm
        recommended_cars = [
            {
                "product_id": result.payload.get("product_id"),
                "product_name": result.payload.get("name"),
                "brand": result.payload.get("keywords", [])[0],
                "price": result.payload.get("additional_info", {}).get("price"),
                "seats": result.payload.get("additional_info", {}).get("seats"),
                "brand": result.payload.get("keywords", [])[4],
                "year": result.payload.get("additional_info", {}).get("year"),
                "score": result.score
            }
            for result in search_results
        ]

        return recommended_cars

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

@app.post("/recommend-cars")
def recommend_cars_endpoint(user_input: UserInput):
    user_input_dict = user_input.model_dump()
    recommendations = recommend_cars(user_input_dict)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No cars found matching the criteria.")
    return {"recommendations": recommendations}
