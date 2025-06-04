@echo off
echo 백엔드 실행 중...
cd backend
call venv\Scripts\activate
start cmd /k "uvicorn main:app --reload"

echo 프론트엔드 실행 중...
cd ../frontend
start cmd /k "npm run dev"
