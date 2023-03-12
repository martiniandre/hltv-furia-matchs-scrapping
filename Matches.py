from bs4 import BeautifulSoup
import urllib.request


def open_page(url: str) -> BeautifulSoup:
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    headers = {'User-Agent': user_agent, }

    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    html_bytes = response.read().decode('utf-8')

    soup = BeautifulSoup(html_bytes, "html.parser")

    return soup


def get_matches_results(result_rows):
    data = []
    for row in result_rows:
        results = row.findAll('td')
        match_data = {"date": None, "win": {}, "lose": {}}
        for result in results:
            match result["class"][0]:
                case "date-cell":
                    match_data["date"] = result.span.string
                case "team-center-cell":
                    [win_data, lose_data] = format_result(result)
                    match_data["win"] = win_data
                    match_data["lose"] = lose_data
        data.append(match_data)
    return data


def format_result(result):
    win_team = result.select('div.team-flex:not(.lost)')[0]
    lost_team = result.select('div.team-flex:is(.lost)')[0]

    win_score = result.select('.score-cell > .score:not(.lost)')[0].string
    lost_score = result.select('.score-cell > .score:is(.lost)')[0].string

    win_data = {
        "team_name": win_team.img["alt"],
        "score": win_score,
        "team_logo": win_team.img["src"]
    }

    lose_data = {
        "team_name": lost_team.img["alt"],
        "score": lost_score,
        "team_logo": lost_team.img["src"]
    }

    return win_data, lose_data
