# 流程圖設計 (Flowchart)

本文件使用 Mermaid 語法描述使用者的操作路徑與系統內部的資料流向。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者進入網站後，可以進行的各項任務管理操作：

```mermaid
flowchart LR
    Start([使用者進入首頁]) --> Home[首頁 - 任務列表]
    
    Home --> Action{要執行什麼操作？}
    
    Action -->|新增| Add[在輸入框填寫任務名稱並送出]
    Add -->|成功| Home
    
    Action -->|切換狀態| Toggle[點擊核取方塊切換狀態]
    Toggle -->|成功| Home
    
    Action -->|編輯| Edit[點擊進入編輯頁面 / 修改文字後送出]
    Edit -->|成功| Home
    
    Action -->|刪除| Delete[點擊垃圾桶圖示]
    Delete -->|成功| Home
    
    Action -->|篩選| Filter[點擊 全部/未完成/已完成 頁籤]
    Filter --> Home
```

## 2. 系統序列圖 (Sequence Diagram)

此圖描述當使用者「新增一個任務」時，系統各個元件如何互動與傳遞資料：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 在表單輸入「寫報告」並點擊新增
    Browser->>Flask: POST /tasks/add (title="寫報告")
    
    Flask->>Flask: 驗證標題不為空
    Flask->>Model: task_model.create("寫報告")
    
    Model->>DB: INSERT INTO tasks (title) VALUES ("寫報告")
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳新建任務的 ID
    
    Flask-->>Browser: HTTP 302 重導向到首頁 (GET /)
    
    Browser->>Flask: GET /
    Flask->>Model: task_model.get_all()
    Model->>DB: SELECT * FROM tasks
    DB-->>Model: 回傳任務列表資料
    Model-->>Flask: 回傳列表資料給路由
    
    Flask->>Flask: 使用 Jinja2 渲染 index.html
    Flask-->>Browser: 回傳渲染後的 HTML
    Browser-->>User: 看到新增完成的任務列表
```

## 3. 功能清單對照表

此表對應了使用者操作與即將實作的 HTTP 路由：

| 功能操作 | HTTP 方法 | URL 路徑 | 對應邏輯與說明 |
| :--- | :--- | :--- | :--- |
| **顯示任務列表** | GET | `/` | 查詢所有任務並渲染首頁清單 (可帶狀態過濾參數) |
| **新增任務** | POST | `/tasks/add` | 接收表單傳來的 `title`，寫入資料庫並重導向首頁 |
| **切換完成狀態** | POST | `/tasks/<id>/toggle` | 更新指定 ID 的 `status` 欄位並重導向首頁 |
| **編輯任務頁面** | GET | `/tasks/<id>/edit` | 顯示該任務的修改表單頁面 |
| **更新任務內容** | POST | `/tasks/<id>/edit` | 接收修改後的 `title`，更新資料庫並重導向首頁 |
| **刪除任務** | POST | `/tasks/<id>/delete` | 刪除指定 ID 的任務記錄並重導向首頁 |
