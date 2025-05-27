# # 과제 1 
# # 학생들의 이름과 점수 정보를 리스트로 관리하는 코드 

# # 기능 
# # 학생 추가: 이름과 점수를 입력 받아 목록에 추가 
# # 학생 삭제: 이름을 입력받아 해당 학생 정보 삭제 
# # 성적 수정: 이름을 입력 받아 해당 학생의 점수 수정 
# # 전체 목록 출력: 모든 학생의 이름과 점수 출력 
# # 통계 출력: 최고 점수, 최저 점수, 평균 점수 계산 및 출력 


# # 이름과 점수 정보 저장할 리스트 생성 
# students = []

# def add_student(): 
#     name = input("\n추가할 학생의 이름을 입력하세요: ")
#     score = float(input("\n점수를 입력하세요: "))
#     students.append({"name":name, "score":score})
#     print(f"\n{name} 학생이 목록에 추가되었습니다.")

# def delete_student(): 
#     name = input("\n삭제할 학생의 이름을 입력하세요: ")
    
#     for student in students:
#         if student in students:
#             students.remove(student)
#             print(f"\n{name} 학생이 목록에서 삭제되었습니다. ")
#             return
#     print(f"\n{name} 학생을 찾을 수 없습니다. ")

# def update_score():
#     name = input("\n점수를 수정할 학생의 이름을 입력하세요: ")

#     for student in students:
#         if student["name"] == name:
#             new_score = float(input(f"\n수정할 점수를 입력하세요: "))
#             student["score"] = new_score
#             print(f"\n{name} 학생의 점수가 수정되었습니다. ")
#             return
#     print(f"\n{name} 학생을 찾을 수 없습니다. ")

# def print_all():
#     if not students:
#         print("\n등록된 학생이 없습니다. ")
#     else: 
#         print("\n전체 학생 목록: \n")
#         for student in students:
#             print(f"이름: {student['name']}, 성적: {student['score']}")

# def print_stat():
#     if not students:
#         print("\n등록된 학생이 없습니다. ")
#         return
    
#     scores = [student['score'] for student in students]
#     max_score = max(scores)
#     min_score = min(scores)
#     avg_score = sum(scores) / len(scores)

#     print(f"최고 점수: {max_score}")
#     print(f"최저 점수: {min_score}")
#     print(f"평균 점수: {avg_score}")

# def main():
#     while True:
#         print("\n==========메뉴==========")
#         print("1. 학생 추가")
#         print("2. 학생 삭제")
#         print("3. 성적 수정")
#         print("4. 전체 목록 출력")
#         print("5. 통계 출력")
#         print("6. 종료")

#         choice = input("\n원하는 기능의 번호를 입력해주세요: ")

#         if choice == "1":
#             add_student()
#         elif choice == "2":
#             delete_student()
#         elif choice == "3":
#             update_score()
#         elif choice == "4":
#             print_all()
#         elif choice == "5":
#             print_stat()
#         elif choice == "6":
#             print("프로그램을 종료합니다.")
#             break
#         else:
#             print("\n올바른 번호를 입력하세요.")

# if __name__ == "__main__":
#     main()


# ================================================================================

# 방법 2: 함수 사용 X

# 학생들의 이름과 점수 정보를 리스트로 관리하는 코드 

# 기능 
# 학생 추가: 이름과 점수를 입력 받아 목록에 추가 
# 학생 삭제: 이름을 입력받아 해당 학생 정보 삭제 
# 성적 수정: 이름을 입력 받아 해당 학생의 점수 수정 
# 전체 목록 출력: 모든 학생의 이름과 점수 출력 
# 통계 출력: 최고 점수, 최저 점수, 평균 점수 계산 및 출력 

# 이름과 점수 정보 저장할 리스트 생성 
students = []

# 메인 루프
while True:
    print("\n==========메뉴==========")
    print("1. 학생 추가")
    print("2. 학생 삭제")
    print("3. 성적 수정")
    print("4. 전체 목록 출력")
    print("5. 통계 출력")
    print("6. 종료")

    choice = input("\n원하는 기능의 번호를 입력해주세요: ")

    if choice == "1":
        name = input("\n추가할 학생의 이름을 입력하세요: ")
        score = float(input("\n점수를 입력하세요: "))
        students.append({"name": name, "score": score})
        print(f"\n{name} 학생이 목록에 추가되었습니다.")

    elif choice == "2":
        name = input("\n삭제할 학생의 이름을 입력하세요: ")
        found = False
        for student in students:
            if student["name"] == name:
                students.remove(student)
                print(f"\n{name} 학생이 목록에서 삭제되었습니다.")
                found = True
                break
        if not found:
            print(f"\n{name} 학생을 찾을 수 없습니다.")

    elif choice == "3":
        name = input("\n점수를 수정할 학생의 이름을 입력하세요: ")
        found = False
        for student in students:
            if student["name"] == name:
                new_score = float(input("\n수정할 점수를 입력하세요: "))
                student["score"] = new_score
                print(f"\n{name} 학생의 점수가 수정되었습니다.")
                found = True
                break
        if not found:
            print(f"\n{name} 학생을 찾을 수 없습니다.")

    elif choice == "4":
        if not students:
            print("\n등록된 학생이 없습니다.")
        else:
            print("\n전체 학생 목록:\n")
            for student in students:
                print(f"이름: {student['name']}, 성적: {student['score']}")

    elif choice == "5":
        if not students:
            print("\n등록된 학생이 없습니다.")
        else:
            scores = [student["score"] for student in students]
            max_score = max(scores)
            min_score = min(scores)
            avg_score = sum(scores) / len(scores)

            print(f"\n최고 점수: {max_score}")
            print(f"최저 점수: {min_score}")
            print(f"평균 점수: {avg_score:.2f}")

    elif choice == "6":
        print("프로그램을 종료합니다.")
        break

    else:
        print("\n올바른 번호를 입력하세요.")
