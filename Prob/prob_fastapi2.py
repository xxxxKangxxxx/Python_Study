# FastAPI 웹 프레임워크, 파일 업로드 및 예외 처리를 위한 모듈 임포트
from fastapi import FastAPI, UploadFile, File, Query, HTTPException

# 파일 응답 처리를 위한 모듈
from fastapi.responses import FileResponse

# 데이터 유효성 검사를 위한 Pydantic 모델 및 필드 유효성 설정 도구
from pydantic import BaseModel, Field

# 타입 힌트(리스트, 옵셔널 등) 제공
from typing import List, Optional

# 파일 복사, 디렉토리 작업, ZIP 압축, UUID 생성에 필요한 표준 라이브러리
import shutil, os, zipfile
import uuid

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="멀티 파일 관리 API",                             # Swagger 제목
    description="파일 업로드, 조회, 다운로드, 삭제 기능 제공",  # Swagger 설명
    version="1.0.0"                                         # API 버전
)

# 업로드 디렉토리 경로 정의
UPLOAD_DIR = "uploads"

# 업로드 디렉토리가 없다면 새로 생성 (오류 방지용)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 허용되는 파일 타입 정의
ALLOWED_FILE_TYPES = {
    "image": ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"],
    "document": [
        "application/pdf", 
        "application/msword", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
        "text/plain"
    ],
    "archive": ["application/zip", "application/x-zip-compressed", "application/x-rar-compressed"],
    "video": ["video/mp4", "video/avi", "video/mov", "video/wmv"],
    "audio": ["audio/mp3", "audio/wav", "audio/ogg", "audio/mpeg"]
}

def validate_file_type(content_type: str) -> bool:
    """파일 타입 검증 함수"""
    allowed_types = []
    for types in ALLOWED_FILE_TYPES.values():
        allowed_types.extend(types)
    return content_type in allowed_types


# 단일/다중 파일 업로드 API 엔드포인트 
@app.post("/upload", tags=["파일 업로드"])
async def upload_files(files: List[UploadFile] = File(...)):
    """
    - 업로드된 파일들을 서버에 저장
    - 파일명 중복 방지를 위해 UUID 접두어 추가
    - 업로드된 파일 목록을 응답으로 반환
    """
    uploaded = []  # 저장된 파일명 리스트 초기화
    errors = [] # 오류 목록 초기화 

    for file in files:
        # 파일 타입 검증
        if not validate_file_type(file.content_type):
            errors.append(f"{file.filename}: 허용되지 않는 파일 타입입니다. ({file.content_type})")
            continue
        
        # 고유한 UUID 기반 파일명 생성
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            # 파일 내용을 실제 서버 디스크에 저장
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            uploaded.append(filename)  # 업로드된 파일명 저장
        except Exception as e:
            errors.append(f"{file.filename}: 파일 저장 중 오류 - {str(e)}")

    # 업로드된 파일이 없고 오류만 있는 경우 예외 발생
    if not uploaded and errors:
        raise HTTPException(status_code=400, detail="; ".join(errors))

    response = {"uploaded_files": uploaded}
    if errors:
        response["errors"] = errors

    return response


# 파일 목록 조회 API 엔드포인트 
# Pydantic 모델로 쿼리 파라미터 유효성 검사용 클래스 정의 (직접 사용하지 않지만 참고용)
class FileListQuery(BaseModel):
    name_filter: Optional[str] = Field(None, description="파일 이름 필터")
    skip: int = Field(0, ge=0, description="페이지 시작 위치")
    limit: int = Field(10, gt=0, description="한 페이지당 항목 수")

@app.get("/files", tags=["파일 조회"])
async def list_files(
    name_filter: Optional[str] = Query(None),  # 이름 필터 (옵션)
    skip: int = 0,                             # 시작 인덱스 (기본값 0)
    limit: int = 10                            # 페이지 크기 (기본값 10)
):
    """
    - 업로드된 파일 목록을 반환
    - 이름 필터링 + 페이지네이션 지원
    """
    files = os.listdir(UPLOAD_DIR)  # 업로드된 모든 파일 리스트 로드

    if name_filter:
        # 필터 문자열이 포함된 파일명만 필터링
        files = [f for f in files if name_filter in f]

    # 페이지네이션 적용 후 결과 반환
    return {
        "files": files[skip: skip + limit],
        "total": len(files)
    }


# 파일 다운로드 API 엔드포인트 
@app.get("/download", tags=["파일 다운로드"])
async def download_files(file_names: List[str] = Query(...)):
    """
    - 단일 파일 다운로드: 개별 파일로 반환
    - 다중 파일 다운로드: ZIP으로 묶어서 반환
    """
    if len(file_names) == 1:
        # 단일 파일 다운로드 처리
        file_path = os.path.join(UPLOAD_DIR, file_names[0])

        if not os.path.exists(file_path):
            # 파일이 존재하지 않을 경우 404 에러 발생
            raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")

        # 파일 응답 반환
        return FileResponse(file_path, filename=file_names[0])

    # 다중 파일을 ZIP으로 압축하여 반환
    zip_path = os.path.join(UPLOAD_DIR, "download.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for name in file_names:
            file_path = os.path.join(UPLOAD_DIR, name)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=name)  # ZIP 내부에는 원래 파일명으로 저장

    return FileResponse(zip_path, filename="files.zip")  # ZIP 파일 응답 반환


# 파일 삭제 API 엔드포인트 
@app.delete("/delete", tags=["파일 삭제"])
async def delete_files(file_names: List[str] = Query(...)):
    """
    - 전달된 파일명을 기준으로 삭제
    - 존재하는 파일만 삭제되고 삭제된 목록 반환
    """
    deleted = []  # 삭제된 파일명 목록

    for name in file_names:
        path = os.path.join(UPLOAD_DIR, name)
        if os.path.exists(path):
            os.remove(path)         # 파일 삭제
            deleted.append(name)    # 삭제 성공한 파일 이름 저장

    return {"deleted": deleted}


# 허용된 파일 타입 조회 API 엔드포인트 
@app.get("/allowed-types", tags=["파일 정보"])
async def get_allowed_file_types():
    """
    - 허용되는 파일 타입 목록 반환
    """
    return {"allowed_file_types": ALLOWED_FILE_TYPES}
