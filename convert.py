# coding=utf-8
__author__ = 'neversmile'

import os
from HTMLParser import HTMLParser

settings = """
*** Settings ***
Resource    seleniumLibrary.txt
Suite Teardown    Close Browser
"""

variables = "*** Variables ***\n"

testcases = "*** Test Cases ***\n"

dem_file = 0 # Dùng để đếm các file mà không ở cùng với folder
dem_file2 = 0 # Dùng để đếm các file mà ở cùng với folder

def process_link(data):
    """

    :rtype : string
    Xu li phan link, tra ve baseURL
    """
    seleniumbase = "('rel', 'selenium.base')('href', '"
    return data[len(seleniumbase):len(data) - 3]


def special_charater(data):
    """
    Xử lí các kí tự đặc biệt
    :param data: là một xâu kí tự, ở đây là data
    :return: trả về một xâu kí tự, nên phải gán bằng với dataưa
    """
    data = data.replace("&quot;", '"')
    data = data.replace('&ndash;', '-')
    data = data.replace('&mdash;', '_')
    data = data.replace("&quot;", '"')
    data = data.replace("&ldquo;", '"')
    data = data.replace('&rsquo;', '\'')
    data = data.replace('&gt;', '>')
    data = data.replace('..','.')
    return data


class RobotHTMLParser(HTMLParser):
    cases = ""  # Xử lí phần test cases
    starttag = ""
    baseURL = "" # Lưu lại đường link đầu tiên
    title = ""
    previous_data = ""  # Để xử lí lệnh open    /...
    previous_two_data = "" # Để xử lí kí tự trống khi type
    check_start_tag = False # Để xử lí kí tự trống khi type

    def handle_starttag(self, tag, attrs):
        self.check_start_tag = True
        self.starttag = tag
        if tag == "link":
            temp = ''
            for attr in attrs:
                temp += str(attr)
            self.baseURL = process_link(temp)

    def handle_data(self, data):
        """
        Hàm handle_data đọc cả các kí tự tab và xuống dòng vì vậy những data mà chứa những kí tự này sẽ bị loại
        Nếu không muốn bỏ như thế này thì file HTML phải viết trên một dòng
        Vì vậy có sử dụng các \n \t in data để loại bỏ những data này
        """
        special_charater(data)
        self.check_start_tag = False
        if self.starttag == "title":
            if "\n" in data or "\t" in data:
                pass
            else:
                self.title = data
                self.cases += data
                # Thêm Open Browser vào mỗi Test Case đầu tiên
                if dem_file == 1 or dem_file2 == 1:
                    self.cases += "\n"
                    self.cases += "    Open Browser    " + self.baseURL + "    firefox"

        if self.starttag == "td":
            # Xử lí phần open   /...
            if "open" in self.previous_data and data[0] == "/":
                data = self.baseURL + data
            # Hết phần xử lí open    /..."

            if "\n" in data or "\t" in data:
                pass
            else:
                if data != self.title:
                    self.cases += "    " + data
                self.previous_two_data = self.previous_data
                self.previous_data = data


    def handle_endtag(self, tag):
        if tag == "tr":
            self.cases += '\n'
        # Sử dụng previous_two_data để thêm các kí tự trống tức là ${EMPTY}
        # Tức là nếu 2 data khác rỗng trước đó có type (mới xử lí được type) và biến check_start_tag đúng
        # (tức là ở giữa starttag và endtag không có data, tức là dữ liệu ô đó bị trống) thì ta thay thế ô đó bằng ${EMPTY}
        if "type" in self.previous_two_data and self.check_start_tag == True:
            self.cases += "    ${EMPTY}"

seleniumLibrary = """
*** Settings ***
Documentation     This resource define keywords of SeleniumHQ in Robot Framework
Library           Selenium2Library

*** Variables ***
${EMPTY}          ""

*** Keywords ***
open
    [Arguments]    ${element}
    Go To    ${element}

clickAndWait
    [Arguments]    ${element}
    Click Element    ${element}

click
    [Arguments]    ${element}
    Click Element    ${element}

type
    [Arguments]    ${element}    ${value}
    Input Text    ${element}    ${value}

selectAndWait
    [Arguments]    ${element}    ${value}
    Select From List    ${element}    ${value}

select
    [Arguments]    ${element}    ${value}
    Select From List    ${element}    ${value}

waitForTextPresent
    [Arguments]    ${text}
    Wait Until Page Contains    ${text}

verifyValue
    [Arguments]    ${element}    ${value}
    Wait Until Page Contains     ${value}
    Element Should Contain    ${element}    ${value}

verifyText
    [Arguments]    ${element}    ${value}
    Wait Until Page Contains    ${value}
    Element Should Contain    ${element}    ${value}

verifyElementPresent
    [Arguments]    ${element}
    Wait Until Page Contains    ${element}
    Page Should Contain Element    ${element}

verifyTextPresent
    [Arguments]    ${element}
    Wait Until Page Contains    ${element}
    Page Should Contain    ${element}

verifyVisible
    [Arguments]    ${element}
    Wait Until Page Contains    ${element}
    Page Should Contain Element    ${element}

verifyTitle
    [Arguments]    ${title}
    Title Should Be    ${title}

verifyTable
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

assertComfirmation
    [Arguments]    ${text}
    Page Should Contain    ${text}

chooseOkOnNextConfirmation
    Choose Ok On Next Confirmation

chooseCancelOnNextConfirmation
    Choose Cancel On Next Confirmation

assertAlert
    [Arguments]    ${text}
    Alert Should Be Present    ${text}

assertText
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

assertValue
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

assertElementPresent
    [Arguments]    ${element}
    Page Should Contain Element    ${element}

assertVisible
    [Arguments]    ${element}
    Page Should Contain Element    ${element}

assertTitle
    [Arguments]    ${title}
    Title Should Be    ${title}

assertTable
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

waitForText
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

waitForValue
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

waitForElementPresent
    [Arguments]    ${element}
    Page Should Contain Element    ${element}

waitForVisible
    [Arguments]    ${element}
    Page Should Contain Element    ${element}

waitForTitle
    [Arguments]    ${title}
    Title Should Be    ${title}

waitForTable
    [Arguments]    ${element}    ${value}
    Element Should Contain    ${element}    ${value}

doubleClick
    [Arguments]    ${element}
    Double Click Element    ${element}

doubleClickAndWait
    [Arguments]    ${element}
    Double Click Element    ${element}

goBack
    Go Back

goBackAndWait
    Go Back

runScript
    [Arguments]    ${code}
    Execute Javascript    ${code}

runScriptAndWait
    [Arguments]    ${code}
    Execute Javascript    ${code}

setSpeed
    [Arguments]    ${value}
    Set Selenium Timeout    ${value}

setSpeedAndWait
    [Arguments]    ${value}
    Set Selenium Timeout    ${value}

vefifyAlert
    [Arguments]    ${value}
    Alert Should Be Present    ${value}
"""

path_hint = "/home/neversmile/Downloads/tests"
answer = ""
while answer != "Y" and answer != "N" and answer != "y" and answer != "n":
    print "Default directory: /home/neversmile/Downloads/tests/"
    answer = raw_input("Do you want to USE default directory?(Y/N)")
if answer == "y" or answer == "Y":
    path = path_hint
else:
    print "Hint: Directory have to end by slash!"
    path = raw_input("Input directory: ")

MAX = 40
matrix_raw = [['' for x in range(MAX)] for x in range(MAX)]

if os.path.exists(path):
    dirs = os.listdir(path)

    path_sol = path + "/Solution"
    # Kiểm tra đường dẫn tồn tại hay chưa, nếu chưa thì tạo nó
    if not os.path.exists(path_sol): os.mkdir(path_sol)

    # Thêm seleniumLibrary.txt
    lib = open(path_sol + "/seleniumLibrary.txt","w")
    lib.write(seleniumLibrary)

    count_html = 0
    dem_file2 = 0
    for f in sorted(dirs):
        sub_dirs = ''
        # Chỉ chọn các folder không chọn các file như html, bat, txt, ini và folder Solution
        if '.html' not in f and '.bat' not in f and '.TXT' not in f and '.ini' not in f and f != "Solution" and '.txt' not in f:
            print f
            # Đường dẫn của các Test Suite
            path_sol_file = path_sol + "/" + f + ".txt"
            suite = open(path_sol_file, "w")
            suite.write(settings)
            suite.write(variables)
            suite.write(testcases)
            a = RobotHTMLParser()
            # Đường dẫn của từng folder chứa các Test Case, tức là các Test Suite
            sub_path = path + "/" + f
            # Cho các folder và file con của đường dẫn sub_p
            sub_dirs = os.listdir(sub_path)
            # Biến dem_file dùng để chọn ra Test Case đầu tiên để cho Open Browser,
            # còn các Test Case sau thì không cần Open Browser
            dem_file = 0
            for file in sorted(sub_dirs):
                dem_file += 1
                pathfile = sub_path + "/" + file
                # Chọn những Test Case (tức là co chứa đuôi html) nhưng không chọn suite.html
                if file.find(".html") >= 0 and file != "suite.html":
                    test = open(pathfile)
                    temp = ""
                    for line in test:
                        temp += line
                    # Xử lí các kí tự đặc biet
                    temp = special_charater(temp)
                    # Hàm feed() dùng để đưa dữ liệu vào đối tượng a, các start tag, data và end tag sẽ được đọc lần lượt,
                    # các hàm handle_starttag, handle_data, handle_endtag sẽ lần lượt được chạy
                    a.feed(temp)
                    test.close()

            suite.write(a.cases)
            suite.close()
        elif f.find(".html") >= 0 and f != "suite.html" and f != "Solution":
            count_html += 1
            dem_file2 += 1
            print f
            # Xử lí tên tệp
            path_temp = path[0:len(path)-1]
            name_file = path_temp[path_temp.rfind("/"):len(path_temp)]

            a = RobotHTMLParser()
            if count_html == 1:
                path_file = path_sol + "/" + name_file + ".txt"
                suite = open(path_file,"w")
                suite.write(settings)
                suite.write(variables)
                suite.write(testcases)

            test = open(path + "/" + f)
            temp = ""
            for line in test:
                temp += line
            temp = special_charater(temp)

            a.feed(temp)
            test.close()

            suite.write(a.cases)

else:
    print "Directory is not availble!"
