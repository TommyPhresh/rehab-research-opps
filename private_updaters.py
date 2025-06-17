import requests, time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Collection of all updaters for private foundations
updaters = [
    tomberg, rmjsf, mli, keck, hanger, beckman, alpert,
    mutual, medline, pfizer, robinson, winn, mvdreyfus, ampsych, vsrf, tmcity
    ]

# Tomberg Family Philanthropies
def tomberg():
    link = "https://www.tombergphilanthropies.org/about-our-grants/"
    if requests.get(link).status_code == 200:
        now = datetime.now()
        if (now.month <= 7) and (now.month <= 7):
            due_date = datetime(now.year, 7, 21)
        else: due_date = datetime(now.year + 1, 7, 21)
        return (
            "Tomberg Family Philanthropies",
            "Tomberg Family Foundation, Tomberg & Brecher Charitable Funds",
            "The Tomberg Family Philanthropies only makes grants to 501(c)(3) nonprofit organizations based in the United States and certain government entities or public institutions in the United States such as public schools and universities. We fund projects worldwide that are run by these organizations. Our grants normally range from $5,000 to $20,000.",
            due_date.strftime("%Y-%m-%d"),
            link, True
            )

# Robert & Mary Jane Smith Foundation
def rmjsf():
    link = "https://www.rmjsfoundation.org/giving"
    now = datetime.now()
    if (now.month < 9):
        due_date = datetime(now.year, 9, 1)
    else: due_date = datetime(now.year + 1, 9, 1)
    return (
        "Robert & Mary Jane Smith Foundation Grant",
        "Robert & Mary Jane Smith Foundation",
        "Founded in 2017, the Robert and Mary Jane Smith Foundation is dedicated to supporting nonprofit institutions based in the United States. Our foundation prioritizes support for the development and education of young people, medical institutions and research, cultural and faith-based organizations, and humanitarian efforts.",
        due_date.strftime("%Y-%m-%d"),
        link, True
        )

# Mind and Life Institute
def mli():
    link = "https://www.mindandlife.org/grants/varela-grants"
    now = datetime.now()
    if (now.month < 9):
        due_date = datetime(now.year, 9, 1)
    else: due_date = datetime(now.year + 1, 9, 1)
    return (
        "Mind & Life Francisco J. Varela Research Grants",
        "Mind & Life Institute",
        """The Mind & Life Francisco J. Varela Research Grants - an important and integral component of Mind & Life's support of contemplative scientists and scholars - are based on neuroscientist and philosopher Francisco J. Varela's belief that contemplative practices offer modern science novel, valuable methods for investigating human experience.
        The Varela Grants fund rigorous examinations of contemplative practices with the ultimate goal that findings derived from such investigations will provide greater insight into contemplative practices and their applications for reducing human suffering and promoting flourishing.
        Proposals are encouraged across broad domains, including: cognitive science, clinical psychology, education, anthropology, neuroscience, health/medical, social science, and humanities. Preference is given to proposals that incorporate first-person contemplative methods (e.g., introspective investigation and reports on subjective experience) into cognitive, behavioral, physiological, clinical, or socio-cultural research. Preference is also given to proposals that have the potential to contribute to interdisciplinary knowledge and to make connections across different disciplines. This grant program encourages the active collaboration of scientists with contemplative scholars/practitioners in all phases of research.""",
        due_date.strftime("%Y-%m-%d"),
        link, True
        )

# Keck Foundatoin
def keck():
    link = "https://www.wmkeck.org/research-overview"
    now = datetime.now()
    if (now.month < 5):
        due_date = datetime(now.year, 5, 1)
    elif (now.month < 11):
        due_date = datetime(now.year, 11, 1)
    else: due_date = datetime(now.year + 1, 5, 1)
    return (
        "W. M. Keck Research Program",
        "The W. M. Keck Foundation",
        "The W. M. Keck Research Program seeks to benefit humanity by supporting Medical Research and Science & Engineering projects that are distinctive and novel in their approach, question the prevailing paradigm, or have the potential to break open new territory in their field.",
        due_date.strftime("%Y-%m-%d"),
        link, True
        )

# Hanger Foundation
def hanger():
    link = "https://www.hangerfoundation.org/impact/grants/"
    now = datetime.now()
    if (now.month < 4):
        due_date = datetime(now.year, 4, 1)
    else: due_date = datetime(now.year + 1, 4, 1)
    return [
        (
            "Hanger Foundation Empowerment Grant",
            "Hanger Foundation",
            "Supporting nonprofit organizations that serve people with physical challenges",
            due_date.strftime("%Y-%m-%d"),
            link, True
            ),
        (
            "Hanger Foundation Veteran Grant",
            "Hanger Foundation",
            "Supporting nonprofit organizations that serve our veterans.",
            due_date.strftime("%Y-%m-%d"),
            link, True)
        ]

# Beckman Foundation
def beckman():
    link = "https://www.beckman-foundation.org/programs/beckman-young-investigator/"
    response = requests.get(link)
    if response.status_code == 200:
        now = datetime.now()
        if (now.month < 8):
            due_date = datetime(now.year, 8, 1)
        else: due_date = datetime(now.year + 1, 8, 1)
        return (
            "Beckman Young Investigator Program",
            "The Arnold & Mabel Beckman Foundation",
            "The Beckman Young Investigator (BYI) Program provides research support to the most promising young faculty members in the early stages of their academic careers in the chemical and life sciences, particularly to foster the invention of methods, instruments, and materials that will open up new avenues of research in science.",
            due_date.strftime("%Y-%m-%d"),
            link, True)

# Warren Alpert Foundation
def alpert():
    link1 = "https://www.warrenalpertfoundation.org/grantees"
    link2 = "https://www.warrenalpertfoundation.org/awards"
    now = datetime.now()
    dues = [datetime(1999, 1, 15), datetime(1999, 4, 15),
            datetime(1999, 7, 15), datetime(1999, 10, 15)]
    for i in range(len(dues)):
        if (now.month <= dues[i].month) and (now.day + 14 < dues[i].day):
            due_date1 = datetime(now.year, dues[i].month, dues[i].day)
            break
    row1 = ("Warren Alpert Foundation: grants over $25,000",
            "Warren Alpert Foundation",
            "The Warren Alpert Foundation accepts grants for medical research, medical education, and in some cases general education and basic human services grants.",
            due_date1.strftime("%Y-%m-%d"),
            link1, True)
    if requests.get(link2).status_code == 200:
        if (now.month < 11):
            due_date2 = datetime(now.year, 11, 1)
        else:
            due_date2 = datetime(now.year + 1, 11, 1)
        row2 = ("The Warren Alpert Distinguished Scholar Award for Neuroscience",
                "Warren Alpert Foundation",
                "These transitional awards are to enable a postdoctoral researcher to advance to become a full-time faculty member at the Assistant Professor level or higher and to promote the development of a laboratory program that will lead to independent funding. The medical school, research institute, or academic hospital appointing the scholar will be awarded $200,000 annually for two years to cover salary, lab costs, and related expenses. Under certain circumstances, the awardee may transfer funding to support their beginning faculty position. Indirect costs of up to 15% of direct costs may be included in the $200,000.",
                due_date2.strftime("%Y-%m-%d"),
                link2, True)
    if row2: return [row1, row2]
    else: return [row1]
    

# Mutual of America
def mutual():
    link = "https://www.mutualofamerica.com/about-us/community-building"
    driver = webdriver.Firefox()
    driver.get(link)
    app_link = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((
            By.PARTIAL_LINK_TEXT,
            'Community Partnership Award Competition Application'))
        )
    app_link = app_link.get_attribute('href')
    now = datetime.now()
    if (now.month < 7) and (now.day + 14 <= 30):
        due_date = datetime(now.year, 7, 1)
    else:
        due_date = datetime(now.year + 1, 7, 1)
    return ("Mutual of America Foundation Community Partnership Award",
            "Mutual of America Foundation",
            """The Mutual of America Foundation Community Partnership Award recognizes outstanding nonprofit organizations in the United States that have shown exemplary leadership by facilitating partnerships with public, private, or social sector leaders who are working together as equal partners, not as donors and recipients, to build a cohesive community that serves as a model for collaborating with others for the greater good.
            Each year, the Mutual of America Foundation sponsors a national competition in which hundreds of organizations demonstrate the value of their partnership to the communities they serve, their ability to be replicated by others, and their capacity to stimulate new approaches to addressing significant social issues.
            """,
            due_date.strftime("%Y-%m-%d"),
            app_link, True)

# Medline Industries
def medline():
    link = "https://www.medline.com/about-us/sustainability/community-engagement/grant-guide"
    now = datetime.now()
    dues = [datetime(1999, 3, 31), datetime(1999, 6, 30),
            datetime(1999, 9, 30), datetime(1999, 12, 31)]
    for i in range(len(dues)):
        if (now.month <= dues[i].month) and (now.day + 14 < dues[i].day):
            due_date = datetime(now.year, dues[i].month, dues[i].day)
            break
        
    return ("Medline: Investigator-Initiated Studies Program",
            "Medline Industries",
            "The IIS program provides support for research that advances scientific and medical knowledge about Medline products and generates promising approaches to medical care. Our support of projects can include direct funding to cover all or a portion of study-related costs, product and safety design input. If the Scientific Review Committee approves an application, execution of an agreement is required for disbursement of funds and/or product, which includes milestones and publishing expectations.",
            due_date.strftime("%Y-%m-%d"),
            link, True)
        

# Pfizer
def pfizer():
    def scrape(soup, data):
        table = soup.find('table', class_='cols-5').find('tbody')
        opps = table.find_all('tr')
        print('now scraping ', len(opps), 'opportunities')
        for opp in opps:
            title = opp.find('td',
                             class_='views-field views-field-title').find('div',
                                class_='compound-name').text.strip()
            grant_type = opp.find('td',
                                  class_='views-field views-field-field-grant-type').text.strip()
            focus = opp.find('td',
                             class_='views-field views-field-field-focus-area').text.strip()
            country = opp.find('td',
                               class_='views-field views-field-field-country').text.strip()
            desc = grant_type + " Grant focusing on " + focus + " in " + country
            due_date = opp.find('td',
                                class_='views-field views-field-field-rfp-loi-due-date').find('time').text.strip()
            link_div = opp.find('td',
                                class_='views-field views-field-title').find('div',
                                    class_='extra-row').find_all('div',
                                        class_='extra-row-wrap')
            for div in link_div:
                link = div.find('a', class_='clinical-link')
                if link:
                    link = link['href']
                    break
            data.append(
                (title, "Pfizer", desc,
                 datetime.strptime(due_date, "%B %d, %Y").strftime("%Y-%m-%d"),
                 link, True)
                )

    driver = webdriver.Firefox()
    driver.get("https://pfizer.com/about/programs-policies/grants/competitive-grants")
    data = []
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((
            By.CLASS_NAME, 'cols-5'))
        )
    page_src = driver.page_source
    soup = BeautifulSoup(page_src, 'html.parser')
    scrape(soup, data)
    while True:
        next_button = driver.find_element(By.XPATH,
                                          '//a[@rel="next"]')
        if next_button.get_attribute('aria-disabled') == 'true':
            print("no pages after the one that's already done")
            break
        driver.execute_script('arguments[0].scrollIntoView(true);', next_button)
        driver.execute_script('arguments[0].click();', next_button)
        print('moving to the next page')
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((
                By.CLASS_NAME, 'cols-5'))
            )
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, 'html.parser')
        scrape(soup, data)
        time.sleep(2)
        
    driver.quit()
    return data 
            

# Robinson Foundation
def robinson():
    response = requests.get("https://www.robinsonfdn.org/grant-requirements")
    if response.status_code == 200:
        now = datetime.now()
        if (now < datetime(now.year, 5, 15)):
            due_date = datetime(now.year, 5, 15)
        elif (now < datetime(now.year, 10, 15)):
            due_date = datetime(now.year, 10, 15)
        else:
            due_date = datetime(now.year + 1, 5, 15)
        return ("Robinson Foundation Grant",
                "Robinson Foundation",
                """Founded in 2016, the mission of the Robinson Foundation is to create meaningful impact through giving back to humanity with good nature and generous hearts. We do this as a family-operated foundation, where each memboer of our board is tasked with seeking out areas of need where our contribution can create real change in the lives of those affected.
                We understand that individuals and organizations encounter circumstances every day that they often can't overcome without assistance from those around them. This hope of making an impact and sharing God's love is what drives us to serve every day.
                """,
                due_date.strftime("%Y-%m-%d"),
                "https://www.robinsonfdn.org/grant-requirements",
                True)

# Robert A. Winn Foundation
def winn():
    now = datetime.now()
    if (now < datetime(now.year, 5, 12)):
        due_date = datetime(now.year, 5, 12)
    else:
        due_date = datetime(now.year + 1, 5, 12)
    return ("Robert A. Winn Excellence in Clinical Trials: Career Development Award",
            "Bristol Myers Squibb Foundation",
            """The Robert A. Winn Excellence in Clinical Trials: Career Development Award (Winn CDA), supported by the Bristol Myers Squibb Foundation, is a 2-yr program designed to support the career development of early-stage investigator physicians who have a demonstrated commitment to transforming and expanding access to the clinical research landscape. They will become community-oriented clinical trialists who will drive improved health outcomes through their research and mentoring. Currently, our clinical research areas include cancer, cardiovascular disease, and immunologic disorders.
            The Winn CDA offers a comprehensive and integrated approach to improving participation in clinical trials through workforce development and mentoring.
            """,
            due_date.strftime("%Y-%m-%d"),
            "https://winnawards.org/winn-cda/",
            True)
                

# May & Victoria Dreyfus Foundation
def mvdreyfus():
    response = requests.get("https://mvdreyfusfoundation.org/application-guidelines")
    if response.status_code == 200:
        now = datetime.now()
        if (now < datetime(now.year, 5, 10)):
            due_date = datetime(now.year, 5, 10)
        elif (now < datetime(now.year, 11, 9)):
            due_date = datetime(now.year, 11, 9)
        else: due_date = datetime(now.year + 1, 5, 10)
        return ("Max and Victoria Dreyfus Foundation Grant",
                "The Max and Victoria Dreyfus Foundation",
                "The Foundation does not establish funding priorities on an annual basis, but rather supports worthwhile activities for which an organization has made a compelling case to receive funding. As a result, Foundation staff cannot advise applicants on the appropriateness of one potential submission over another. Instead, we generally suggest that organizations select programs for which they can make their best case for support, and for which a small amount of money can have a large impact.",
                due_date.strftime("%Y-%m-%d"),
                "https://mvdreyfusfoundation.org/application-guidelines",
                True)

# American Psychological Foundation
def ampsych():
    # get all opps from a page
    def extract_opps(soup, data):
        grid = soup.find('div', class_='grid')
        opps = grid.find_all('a')
        for opp in opps:
            link = opp['href']
            title = opp.find('h4').text.strip()
            desc = opp.find('div',
                            class_='text-lg text-gray-900').find('p').text.strip()
            due_date = opp.find('div',
                                class_='transition-all duration-150 mt-3 text-gray-600 text-lg').text.strip()
            due_date = due_date.replace("Deadline: ", "")
            data.append((title, "American Psychological Foundation",
                         desc, due_date, link, True))

    # meat of scraper - webdriver
    driver = webdriver.Firefox()
    driver.get("https://ampsychfdn.org/funding/")
    data = []
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((
            By.CLASS_NAME, 'grid'))
        )
    # scrape first page
    page_src = driver.page_source
    soup = BeautifulSoup(page_src, 'html.parser')
    extract_opps(soup, data)
    # loop through all other pages
    while True:
        try:
            next_button = WebDriverWait(driver, 10).until(
                expected_conditions.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(text(), 'Next')]"))
                )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((
                    By.CLASS_NAME, 'grid'))
                )
            page_src = driver.page_source
            soup = BeautifulSoup(page_src, 'html.parser')
            extract_opps(soup, data)
            time.sleep(2)
        except Exception as e:
            break
    driver.quit()
    return data
    
    

# Virginia Sargeant Reynolds Foundation
def vsrf():
    now = datetime.now()
    if (now.month >= 5) and (now.month < 9):
        due_date = datetime(now.year, 9, 1)
    elif (now.month >= 9):
        due_date = datetime(now.year + 1, 5, 1)
    else:
        due_date = datetime(now.year, 5, 1)
    return ("Virginia Sargeant Reynolds Foundation Grant",
            "Virginia Sargeant Reynolds Foundation",
            """Our mission is to support programs, causes, and organizations within Arts, Education, Environment, Health, History, and Humanity, disciplines which resonated with Virginia Reynolds during her lifetime. The Foundation prioritizes support for causes with a connection to the Commonwealth of Virginia and will selectively support broader domestic and global causes within the six focus disciplines. The Foundation also actively seeks to support causes with a connection to current and future generations of the Reynolds family which are consistent with the Foundation's mission.
            The intellect, thrift, stewadship, and generosity of Virginia Reynolds provided the resources enabling this Foundation to impact the Commonwealth of Virginia and beyond. The Foundation is dedicated to honoring her life and the Reynolds family tradition of service and philanthropy.
            """,
            due_date.strftime("%Y-%m-%d"),
            "https://app.vsrfoundation.com/how-to-apply/",
            True)

# TMCity Foundation
def tmcity():
    response = requests.get("https://www.tmcity.org/foundation")
    
    if response.status_code == 200:
        now = datetime.now()
        if (now.month > 4) and (now.month < 11):
           due_date = datetime(now.year, 10, 31)
        elif (now.month >= 11):
            due_date = datetime(now.year + 1, 4, 30)
        else:
            due_date = datetime(now.year, 4, 30)
        return ("TMCity Foundation: Research",
                "TMCity Foundation",
                """We believe that mental health presents a critical challenge to our society today, and understanding the brain holds the key. While significant medical achievements have been made treating many physical diseases, there is still so much we don't know about the brain and mental health. With technology and data avaiable as never before, real progress in this field is possible, but it requires our attention and financial commitment.
                Catalyzing research efforts is critical to removing stigma and delivering proper care at every stage of life. TMCity is looking for cutting-edge research opportunities and transformative technologies that can advance our understanding of the brain and create innovative, real-world solutions to neurocognitive healthcare problems.
                With a rich heritage of philanthropy, it is our honor and privilege to leverage our resources and expertise to help develop treatments and cures for brain-related ailments.
                """,
                due_date.strftime("%Y-%m-%d"),
                "https://www.tmcity.org/foundation",
                True)
        
