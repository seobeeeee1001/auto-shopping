
import json


class Review:
    def __init__(self, review_id, review_content, rating=None, date=None):
        self.review_id = review_id  # 리뷰 ID (고유값)
        self.review_content = review_content  # 리뷰 내용
        self.date = date  # 작성 날짜 (선택)

    def to_dict(self):
        return {
            "review_id": self.review_id,
            "text": self.review_content,
            "date": self.date,
        }
        
def save_reviews_to_json(reviews, filename="reviews.json"):
    """리뷰 데이터를 JSON 파일로 저장"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([review.to_dict() for review in reviews], f, ensure_ascii=False, indent=4)
