from datetime import datetime
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from review_manager import Review,save_reviews_to_json
import re

def scroll_down(driver, num=1):
    """페이지 아래로 스크롤"""
    try:
        print(f"[DEBUG] {num}번 페이지 스크롤")
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(num):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
    except Exception as e:
        print(f"[오류] 스크롤 실패: {e}")

def navigate_to_reviews(driver):
    """리뷰 페이지로 이동"""
    try:
        print("[DEBUG] 리뷰 페이지로 이동 시도")
        scroll_until_element_visible(driver, By.CSS_SELECTOR, '#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a', 10)
        scroll_down(driver, 5)
        review_tab = wait_for_interactable(driver, By.CSS_SELECTOR, '#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a')
        review_tab.click()
        print("[성공] 리뷰 페이지 이동")
        time.sleep(3)
    except NoSuchElementException:
        print("[오류] 리뷰 탭을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[오류] 리뷰 페이지 이동 실패: {e}")

def page_handle(driver, num):
    try:
        if(num == "다음") :
            print(f"[DEBUG] 페이지 {num} 버튼 클릭 시도")
            scroll_until_element_visible(driver, By.CSS_SELECTOR, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div')
            button = wait_for_element(driver, By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a.fAUKm1ewwo._2Ar8-aEUTq._nlog_click')
            print("[성공] 버튼이 발견되었습니다!")
            button.click()
            time.sleep(3)
        else :
            print(f"[DEBUG] 페이지 {num} 버튼 클릭 시도")
            scroll_until_element_visible(driver, By.CSS_SELECTOR, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div')
            button = wait_for_element(driver, By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({num})')
            print("[성공] 버튼이 발견되었습니다!")
            button.click()
            time.sleep(3)
            return 0
        
    except Exception as e:
        print(f"[오류] 페이지 {num} 버튼 클릭 실패: {e}")
        return 1

def scroll_until_element_visible(driver, by, value, max_scrolls=10, delay=0.5):
    for _ in range(max_scrolls):
        try:
            print(f"[DEBUG] {value} 요소 스크롤로 검색")
            element = wait_for_element(driver, by, value, 1)
            print("[성공] 요소가 발견되었습니다!")
            return element
        except Exception as e:
            print(f"[알림] 요소를 아직 찾지 못했습니다. 스크롤 중. 오류: {e}")
            scroll_down(driver, 1)
            time.sleep(delay)  # 스크롤 후 잠시 대기
    
    print("[실패] 지정된 요소를 찾지 못했습니다.")
    return None

def wait_for_interactable(driver,by,value,timeout=10):
    try:
        print(f"[DEBUG] {value} 클릭 가능 대기 중")
        return WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
    except Exception as e:
        print(f"[오류] 클릭 가능 대기 실패: {e}")
        raise

def wait_for_element(driver, by, value, timeout=10):
    """특정 요소가 나타날 때까지 대기"""
    try:
        print(f"[DEBUG] {value} 요소 대기 중")
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        print(f"[오류] 요소 대기 실패: {e}")
        raise

def open_website(driver, url):
    """웹사이트 열기"""
    try:
        print("[DEBUG] 웹사이트 열기 시도:", url)
        driver.get(url)
        print("[성공] 웹사이트 열기")
    except Exception as e:
        print(f"[오류] 웹사이트 열기 실패: {e}")
        raise
    
def review_extract(driver,start_id):
    
    
    try:      
        review_list = []
        print("[DEBUG] 리뷰 추출 시작")         
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        time.sleep(0.5)
        reviews = soup.findAll('li', {'class': 'BnwL_cs1av'})   
        if not reviews:
            print("[알림] 리뷰를 찾을 수 없습니다.")
        for idx,review in enumerate(reviews):
            # 4-1.리뷰작성일자 수집
            write_dt_raw = review.findAll('span' ,{'class' : '_2L3vDiadT9'})[0].get_text()
            write_dt = datetime.strptime(write_dt_raw, '%y.%m.%d.').strftime('%Y%m%d')

            # 4-3. 리뷰내용 수집
            review_content_raw = review.findAll('div', {'class' : '_1kMfD5ErZ6'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
            review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))

            review_id = start_id + idx
            
            # 4-4. 수집데이터 저장
            review_obj = Review(review_id=review_id, review_content=review_content,date=write_dt)
            review_list.append(review_obj)
        
        return review_list, start_id + len(reviews)
       
        
    except Exception as e:
        print(f"[오류] 리뷰 추출 실패: {e}")
    
    return review_list