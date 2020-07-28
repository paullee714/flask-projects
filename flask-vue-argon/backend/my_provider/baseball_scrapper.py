import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, 팀순위 표를 가져오기
ranking_table = soup.select('#regularTeamRecordList_table > tr')
# print(ranking_table)

def get_baseball_rank():

    result_list = []
    for ranking_info in ranking_table:
        data_dict = {}

        img_url = ranking_info.select_one('td.tm > div > img')['src']
        rank = ranking_info.select_one('th > strong').text
        name = ranking_info.select_one('td.tm > div > span').text
        win_rate = ranking_info.select_one('td:nth-child(7) > strong').text
        total_cnt = ranking_info.select_one('td:nth-child(3) > span').text
        total_win = ranking_info.select_one('td:nth-child(4) > span').text
        total_lose = ranking_info.select_one('td:nth-child(5) > span').text
        total_draw = ranking_info.select_one('td:nth-child(6) > span').text
        total_diff = ranking_info.select_one('td:nth-child(8) > span').text
        total_run = ranking_info.select_one('td:nth-child(10) > span').text
        recent_ten_game = ranking_info.select_one('td:nth-child(12) > span').text

        data_dict['img_url'] = img_url
        data_dict['rank'] = rank
        data_dict['name'] = name
        data_dict['win_rate'] = win_rate
        data_dict['total_cnt'] = total_cnt
        data_dict['total_win'] = total_win
        data_dict['total_lose'] = total_lose
        data_dict['total_draw'] = total_draw
        data_dict['total_diff'] = total_diff
        data_dict['total_run'] = total_run
        data_dict['recent_ten_game'] = recent_ten_game

        result_list.append(data_dict)

    return result_list
