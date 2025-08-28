# 使用官方 Python 3.11 slim 版本作為基底映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY main.py .

# 暴露應用程式使用的埠號
EXPOSE 8000

# 定義容器啟動時執行的命令
CMD ["python", "main.py"]