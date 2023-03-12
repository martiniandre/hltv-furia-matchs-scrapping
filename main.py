import Matches


def main():
    url = "https://www.hltv.org/team/8297/furia#tab-matchesBox"
    soup = Matches.open_page(url)
    result_rows = soup.find_all('tr', {"class": "team-row"})
    result_data = Matches.get_matches_results(result_rows)
    print(result_data)


main()
