from data import article_metadata, ask_search, ask_advanced_search
import datetime
import time


def keyword_to_titles(metadata):
    new_dict = {}
    for item in metadata:
        for keyword in item[4]:
            if keyword not in new_dict:
                new_dict[keyword] = [item[0]]
            else:
                new_dict[keyword].append(item[0])
    return new_dict


def title_to_info(metadata):
    new_dict = {}
    for item in metadata:
        new_dict[item[0]] = {'author': item[1], 'timestamp': item[2], 'length': item[3]}

    return new_dict


def search(keyword, keyword_to_titles):
    if keyword in keyword_to_titles:
        return keyword_to_titles[keyword]
    return []


def article_length(max_length, article_titles, title_to_info):
    final_list = []
    for item in article_titles:
        if title_to_info[item]['length'] <= max_length:
            final_list.append(item)
    return final_list


def key_by_author(article_titles, title_to_info):
    final_dict = {}
    for item in article_titles:
        if title_to_info[item]['author'] not in final_dict:
            final_dict[title_to_info[item]['author']] = [item]
        else:
            final_dict[title_to_info[item]['author']].append(item)
    return final_dict


def filter_to_author(author, article_titles, title_to_info):
    final_list = []
    for item in article_titles:
        if title_to_info[item]['author'] == author:
            final_list.append(item)
    return final_list


def filter_out(keyword, article_titles, keyword_to_titles):
    if keyword not in keyword_to_titles:
        return article_titles
    new_article_list = keyword_to_titles[keyword]
    final_list = []
    for item in article_titles:
        if item not in new_article_list:
            final_list.append(item)
    return final_list


def articles_from_year(year, article_titles, title_to_info):
    final_list = []
    first_day_year = datetime.date(year, 1, 1)
    last_day_year = datetime.date(year, 12, 31)
    first_timestamp = time.mktime(first_day_year.timetuple())
    last_timestamp = time.mktime(last_day_year.timetuple())
    for item in article_titles:
        if first_timestamp <= title_to_info[item]['timestamp'] <= last_timestamp:
            final_list.append(item)
    return final_list


def display_result():
    keyword_to_titles_dict = keyword_to_titles(article_metadata())
    title_to_info_dict = title_to_info(article_metadata())

    articles = search(ask_search(), keyword_to_titles_dict)

    advanced, value = ask_advanced_search()

    if advanced == 1:
        articles = article_length(value, articles, title_to_info_dict)
    if advanced == 2:
        articles = key_by_author(articles, title_to_info_dict)
    elif advanced == 3:
        articles = filter_to_author(value, articles, title_to_info_dict)
    elif advanced == 4:
        articles = filter_out(value, articles, keyword_to_titles_dict)
    elif advanced == 5:
        articles = articles_from_year(value, articles, title_to_info_dict)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))


display_result()
