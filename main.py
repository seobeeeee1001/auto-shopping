from selenium import webdriver
from scraper import open_website
from scraper import navigate_to_reviews
from scraper import review_extract
from scraper import page_handle
from scraper import navigate_to_reviews
from review_manager import Review,save_reviews_to_json

def main():
    """메인 실행 함수"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # 브라우저 창 최대화
    driver = webdriver.Chrome(options=options)
    
    all_reviews = [] 
    start_id = 1  

    try:
        url = "https://brand.naver.com/basic-s/products/11149376385?nl-query=%EB%85%B8%ED%8A%B8%EB%B6%81"
        open_website(driver, url)

        # 리뷰 페이지 이동
        navigate_to_reviews(driver)
        
        cur_page = 2
        ctrl_page = 2
        page_not_found = 0
        
        while True:
            reviews, start_id = review_extract(driver,start_id)
            all_reviews.extend(reviews)
            ctrl_page += 1
            if(ctrl_page % 12 == 0) : 
                page_handle(driver,"다음")
                continue
            if(ctrl_page == 13) : 
                ctrl_page = 3    
            page_not_found = page_handle(driver, ctrl_page)
            if page_not_found == 1: break
        
        save_reviews_to_json(all_reviews)


    except Exception as e:
        print(f"[오류] 전체 과정 중 문제 발생: {e}")
    finally:
        input("브라우저를 닫으려면 Enter를 누르세요.")
        driver.quit()


if __name__ == "__main__":
    main()
