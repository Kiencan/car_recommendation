from typing import List, Optional
from pydantic import BaseModel, Field

# Pydantic models for request data


class ProfileRequest(BaseModel):
    profile_id: str
    page_view_keywords: List[str]
    purchase_keywords: List[str]
    interest_keywords: List[str]
    additional_info: dict
    max_recommendation_size: int = Field(
        8, description="Default recommendation is 8")
    except_product_ids: List[str] = []
    journey_maps: List[str] = []


class ProductRequest(BaseModel):
    product_id: str
    product_name: str
    url: str = Field('', description="Default is empty")
    product_category: str
    product_keywords: List[str]
    additional_info: dict
    journey_maps: List[str] = []


class ContentRequest(BaseModel):
    content_id: str
    title: str
    description: str
    content: str = Field('', description="Default is empty")
    content_type: str = Field('text', description="Default is text")
    url: str = Field('', description="Default is empty")
    content_category: str
    content_keywords: List[str]
    additional_info: dict
    journey_maps: List[str] = []

class CarPreferences(BaseModel):
    seats: Optional[int] = None
    color: Optional[str] = None
    condition: Optional[str] = None
    brand: Optional[str] = None
    year: Optional[int] = None
    keywords: Optional[List[str]] = None