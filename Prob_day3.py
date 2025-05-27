# Day3

# 클래스와 객체지향 
# 과제: 도서관 시스템 구현 

# 다음 클래스를 구현하세요:
# • `Book`: 도서 정보(제목, 저자, ISBN, 출판연도 등)를 관리
# • `Library`: 도서 컬렉션을 관리하고 대출/반납 기능 제공
# • `Member`: 도서관 회원 정보와 대출 목록 관리

# • 다음 기능을 구현하세요:
# • 도서 추가/삭제
# • 도서 검색(제목, 저자, ISBN으로)
# • 도서 대출/반납
# • 회원 등록/관리
# • 회원별 대출 현황 확인

# • 객체 지향 설계 원칙(SOLID)을 최소한 2가지 이상 적용하세요.

# • 적절한 캡슐화를 통해 데이터를 보호하세요.

class Book: 
    def __init__(self, title, author, isbn, year):
        # Book 객체가 생성될 때, 아래 정보를 받아 초기화 
        self.__title = title 
        self.__author = author
        self.__isbn = isbn
        self.__year = year
        self.__is_borrowed = False # 도서 대출 상태 

    def get_title(self):
        return self.__title # 제목 
    
    def get_author(self):
        return self.__author # 저자 
    
    def get_isbn(self):
        return self.__isbn # ISBN(도서번호)
    
    def get_year(self):
        return self.__year # 출판연도 
    
    def is_borrowed(self):
        return self.__is_borrowed # 대출 여부 (대출되지 않은 상태가 기본값)
    
    def borrow(self): # 도서 대출 확인 
        if self.__is_borrowed: # True: 대출 중인 상태라면 아래 코드 실행 
            # 이미 대출 중이라면 예외 처리 
            raise Exception(f"'{self.__title}'은 대출 중입니다. ")
        
        self.__is_borrowed = True # 대출 상태 처리 

    def return_book(self): # 반납 처리 
        self.__is_borrowed = False # False: 대출 상태 해제


class Library:
    def __init__(self):
        self.__books = [] # 도서 목록을 저장하는 리스트 생성
        self.__members = {} # 회원 정보를 저장하는 딕셔너리 (key: 회원 ID, value: Member 객체)

    def add_book(self, book): # 도서 추가 
        self.__books.append(book)

    def delete_book(self, isbn): # ISBN을 기준으로 도서 삭제 
        # 리스트 컴프리헨션 사용 / 해당 ISBN이 아닌 책들을 새 리스트에 저장 (일치하지 않는 도서만 남기는 방식)
        self.__books = [book for book in self.__books if book.get_isbn() != isbn]

    def search_book(self, keyword, key="title"):
        # 제목을 기본 키로 도서를 검색 (기본값: 제목)
        if key == "title":
            # 제목에 keyword가 포함된 도서 리스트를 반환 
            return [b for b in self.__books if keyword.lower() in b.get_title().lower()]
        elif key == "author":
            # 저자명에 keyword가 포함된 책 반환 
            return [b for b in self.__books if keyword.lower() in b.get_author().lower()]
        elif key == "isbn":
            # ISBN이 정확히 일치하는 책 반환 
            return [b for b in self.__books if keyword == b.get_isbn()]
        else:
            return []
        
    def register_member(self, member): # 새로운 회원 등록 
        # member 딕셔너리에 member_id를 키로 member 객체를 저장 
        self.__members[member.get_id()] = member

    def get_member(self, member_id):
        # member_id로 회원 반환 
        return self.__members.get(member_id)

    def borrow_book(self, member_id, isbn): # 도서 대출 
        member = self.get_member(member_id) # 회원 받아오기 
        book = next((b for b in self.__books if b.get_isbn() == isbn), None) # ISBN으로 도서 찾기 
        if member and book: # 회원과 도서가 모두 존재한다면
            member.borrow_book(book) # Member 클래스의 borrow_book이 실행되면서 도서가 대출됨 -> 도서 대출 처리가 위임되었다고 말함
    
    def return_book(self, member_id, isbn): # 도서 반납 
        member = self.get_member(member_id) # 회원 받아오기 

        if member: # 만약 회원이 있다면 
            # 해당 회원이 대출 중인 도서 중 ISBN이 일치하는 도서 찾기 
            book = next((b for b in member.get_borrowed_books() if b.get_isbn() == isbn), None)
            if book: # 만약 도서가 있다면 
                member.return_book(book) # 도서 반납 처리 위임 
    
    def print_member_status(self, member_id): # 회원의 대출 목록 출력 
        member = self.get_member(member_id) # 회원 받아오기 

        if member: # 만약 회원이 있다면 
            print(f"{member.get_name()}님의 대출 목록: ") 
            for book in member.get_borrowed_books(): # 대출 중인 도서를 순회하며 출력
                print(f" - {book.get_title()} by {book.get_author()}")

class Member:
    def __init__(self, name, member_id):
        self.__name = name # 회원 이름 
        self.__member_id = member_id # 회원 ID
        self.__borrowed_books = [] # 대출한 도서 저장할 리스트 생성 

    def get_name(self):
        return self.__name # 이름 반환 
    
    def get_id(self):
        return self.__member_id # 회원 ID 반환 
    
    def get_borrowed_books(self): 
        return self.__borrowed_books # 대출 중인 도서 리스트 반환 
    
    def borrow_book(self, book): # 도서 대출 함수 
        book.borrow() # Book 클래스에서 도서 상태 변경 처리 
        self.__borrowed_books.append(book) # 도서 대출 리스트에 추가 

    def return_book(self, book): # 도서 반납 함수 
        if book in self.__borrowed_books: # 만약에 책이 도서 대출 리스트에 있다면 
            book.return_book() # Book 클래스에서 도서 반납 처리 
            self.__borrowed_books.remove(book) # 리스트 목록에서 제거 

# =====================================================================================

# 과제: 파일 처리기 구현
#  
# 다양한 유형의 파일(텍스트, CSV, JSON, 바이너리)을 읽고 쓸 수 있어야 합니다
# 파일이 존재하지 않거나, 권한이 없거나, 형식이 잘못된 경우 등 다양한 오류 상황을 적절히 처리
# 사용자 정의 예외 계층 구조를 설계하고 구현
# 오류 발생 시 로깅을 통해 문제를 기록
# 모든 파일 작업은 컨텍스트 매니저(`with` 구문)를 사용

import os
import csv
import logging
import json

# Logging 구현 

logging.basicConfig(
    filename='app.log', # 로그를 기록할 파일 이름 설정 
    level=logging.DEBUG, # DEBUG를 기준으로 로그 기록 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", # 로그 메시지 출력 형식 지정 
    encoding='utf-8' # 로그 파일 인코더 한글이 포함 가능하도록 설정 
)

# 사용자 정의 예외 계층 
class FileError(Exception): # 모든 사용자 정의 예외의 부모 클래스 
    """모든 파일 처리 관련 예외의 기반 클래스""" # 이후 예외들이 해당 클래스를 상속받기에, except FileError 하나로 모든 파일 관련 예외를 처리할 수 있음
    pass

class FileNotFound(FileError): # 파일이 존재하지 않을 때 발생하는 사용자 정의 예외
    """파일이 존재하지 않을 때 발생하는 예외"""
    pass

class FilePermissionError(FileError): # 파일에 접근 권한이 없을 때 발생하는 사용자 정의 예외 
    """파일의 권한의 문제가 있을 때 발생하는 예외"""
    pass

class FileFomatError(FileError): # 파일의 형식이 지원하지 않는 형식일 때 발생하는 사용자 정의 예외 
    """파일의 형식이 지원하지 않을 때 발생하는 예외"""
    pass

# 파일 처리기 
class FileHandler: # 다양한 파일 타입을 읽고 쓸 수 있는 범용 파일 처리 클래스 
    
    # 생성자 함수 
    def __init__(self, filepath, mode, filetype="text"):
        
        self.filepath = filepath # 읽고 쓰기 위한 파일의 경로 
        self.mode = mode # open할 때 사용할 모드 ('r', 'w', 'rb', 'wb' 등)
        self.filetype = filetype # 파일 타입
        self.file = None # 파일 객체를 저장할 변수 

    # with 구문(컨텍스트 매니저) 진입 시 실행됨 
    # 파일을 열고, 파일 객체를 self.file에 저장하고, 자기 자신(self)를 반환
    def __enter__(self): # 입력 함수 
        """with 구문 진입 시 실행되는 메서드"""
        try:
            self.file = open( # open 함수로 파일을 열기 
                self.filepath, # 파일 경로 
                self.mode, # 사용할 모드 
                # 텍스트, JSON, CSV 파일을 읽기 위한 인코더 지정 / binary 파일의 경우 인코더가 없어야 함
                encoding="utf-8" if self.filetype in ['text', 'json', 'csv'] else None 
            )
            return self
        
        except FileNotFoundError: # open() 중에 파일이 존재하지 않는 경우 예외 처리 및 로깅 
            logging.error(f"파일을 찾을 수 없습니다. {self.filepath}")
            raise FileNotFound
        
        except PermissionError: # 파일 접근 권한이 없을 경우 예외 처리 및 로깅 
            logging.error(f"파일 접근 권한 오류입니다. {self.filepath}")
            raise FilePermissionError
        

    # with 구문(컨텍스트 매니저) 종료 시 실행
    def __exit__(self, exc_type, exc_value, traceback): # Python에서는 __exit__() 메서드는 반드시 3개의 인지를 받도록 되어있음 (실행은 안될 수 O)
        """with 구문 종료시 실행되는 메서드""" 
        if self.file:
            self.file.close() # 열린 파일이 있다면 닫음 

    # 파일 읽기 함수 
    def read(self): 
        """파일 읽기 가능 / 다양한 형식의 파일에 맞게 적절한 방식으로 읽기"""
        try:
            if self.filetype == "text": # 일반 텍스트 파일이라면 
                return self.file.read() # file.read()로 전체를 읽음 
            
            elif self.filetype == "json": # 만약 JSON 파일이라면 
                return json.load(self.file) # json.load(file)을 사용해 Python 객체로 변환함 

            elif self.filetype == "csv": # 만약 CSV 파일이라면 
                return list(csv.reader(self.file)) # csv.reader(file)로 읽고 list로 변환해서 반환
            
            elif self.filetype == "binary": # 이진 파일 이라면 
                return self.file.read() # .read()로 바이트 단위로 읽음 
            
            else: # 위의 형식들이 아니라면 예외 처리 
                raise FileFomatError(f"지원하지 않는 파일 형식입니다: {self.filetype}")
            
        except Exception as e: # 예외가 발생했을 때 로그 기록 후 예외 전파 
            logging.error(f"파일 읽기 실패: {e}")
            raise

    # 파일 쓰기 함수: 
    # 파이썬에서 다룰 수 있는 데이터를 해당 파일 형식에 맞는 실제 파일 형태로 변환해서 저장하는 기능을 수행하는 함수 
    def write(self, data):
        """파일 쓰기 가능 / 다양한 형식의 파일에 맞게 적절한 방식으로 입력 """
        try:
            if self.filetype == "text": # 텍스트라면 문자열을 텍스트 파일에 직접 작성 
                self.file.write(data)

            elif self.filetype == "json": # Python 객체를 JSON 형식으로 변환 후 저장 
                json.dump(data, self.file, ensure_ascii=False, indent=2) # ensure_ascii=False: 한글 깨짐 방지 / indent=2: 들여쓰기 사용
            
            elif self.filetype == "csv": # 리스트 형태 데이터를 CSV로 저장 
                writer = csv.writer(self.file)
                writer.writerows(data)

            elif self.filetype == "binary": # 이진 데이터는 그대로 저장 
                self.file.write(data)

            else: # 위와 동일 
                raise FileFomatError(f"지원하지 않는 파일 형식입니다: {self.filetype}")
            
        except Exception as e: # 위와 동일 
            logging.error(f"파일 쓰기 실패: {e}")
            raise