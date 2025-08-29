from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import os

app = FastAPI(title="水果庫存管理系統", description="用於教學 FastAPI 與 Docker 的簡易專案")

DATABASE_FILE = "database.txt"

class FruitUpdate(BaseModel):
    quantity: int

def read_database() -> Dict[str, int]:
    """從文字檔案讀取水果庫存資料"""
    if not os.path.exists(DATABASE_FILE):
        return {}
    
    fruits = {}
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    name, quantity = line.split(':', 1)
                    fruits[name.strip()] = int(quantity.strip())
    except Exception as e:
        print(f"讀取資料庫時發生錯誤: {e}")
        return {}
    
    return fruits

def write_database(fruits: Dict[str, int]):
    """將水果庫存資料寫入文字檔案"""
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
            for name, quantity in fruits.items():
                file.write(f"{name}: {quantity}\n")
    except Exception as e:
        print(f"寫入資料庫時發生錯誤: {e}")

@app.get("/")
def read_root():
    """首頁端點"""
    return {"message": "歡迎使用水果庫存管理系統！"}

@app.get("/fruits/")
def get_all_fruits():
    """取得所有水果庫存"""
    fruits = read_database()
    if not fruits:
        return {"message": "目前沒有水果庫存", "fruits": {}}
    return {"fruits": fruits}

@app.get("/fruits/{fruit_name}")
def get_fruit(fruit_name: str):
    """取得特定水果的庫存"""
    fruits = read_database()
    if fruit_name not in fruits:
        raise HTTPException(status_code=404, detail=f"找不到水果: {fruit_name}")
    return {"fruit": fruit_name, "quantity": fruits[fruit_name]}

@app.get("/fruits/{fruit_name}/updates/{quantity}")
def update_fruit(fruit_name: str, quantity: int):
    """更新特定水果的庫存"""
    fruits = read_database()
    fruits[fruit_name] = quantity
    write_database(fruits)
    return {"message": f"{fruit_name} 庫存已更新", "fruit": fruit_name, "quantity": quantity}

@app.delete("/fruits/{fruit_name}")
def delete_fruit(fruit_name: str):
    """刪除特定水果"""
    fruits = read_database()
    if fruit_name not in fruits:
        raise HTTPException(status_code=404, detail=f"找不到水果: {fruit_name}")
    
    del fruits[fruit_name]
    write_database(fruits)
    return {"message": f"{fruit_name} 已從庫存中移除"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)