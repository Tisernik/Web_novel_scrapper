from get_html import fetch_and_save_html

main_page_url = "https://freewebnovel.com/novel/swallowed-star-2-land-of-origin"  # Replace with the actual URL
file_name = 'MainPage.html'


def main(url, file_name):
    
    html_code = fetch_and_save_html(url, file_name)
    if html_code:
        print(html_code)

if __name__ == "__main__":
    main(main_page_url, file_name)
