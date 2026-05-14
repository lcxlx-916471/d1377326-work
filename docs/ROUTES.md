# 路由與頁面設計 (API Design)

本文件規劃了系統中所有的 URL 路徑與對應的處理邏輯，並定義所需的 HTML 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與任務清單** | GET | `/` | `tasks/index.html` | 顯示所有任務。可接收 `?status=` 參數進行過濾 |
| **新增任務** | POST | `/tasks/add` | — | 接收表單 `title`，成功後重導向 `/` |
| **切換完成狀態** | POST | `/tasks/<int:id>/toggle` | — | 更新特定 ID 的狀態，成功後重導向 `/` |
| **編輯任務頁面** | GET | `/tasks/<int:id>/edit` | `tasks/edit.html` | 顯示特定任務的修改表單 |
| **更新任務內容** | POST | `/tasks/<int:id>/edit` | — | 接收表單修改後的 `title`，更新後重導向 `/` |
| **刪除任務** | POST | `/tasks/<int:id>/delete` | — | 刪除特定 ID 的任務，成功後重導向 `/` |

> **注意**：根據 REST 慣例，刪除與更新應使用 `DELETE` 與 `PUT`/`PATCH`，但由於傳統 HTML 表單只支援 `GET` 與 `POST`，在此我們一律使用 `POST` 來處理狀態變更的操作。

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**：URL 參數 `status` (可選，值為 `0` 或是 `1`)。
- **處理邏輯**：呼叫 `TaskModel.get_all(status)` 取得資料。
- **輸出**：渲染 `tasks/index.html` 並傳入 `tasks` 變數與當前的 `status`。

### `POST /tasks/add`
- **輸入**：表單欄位 `title` (必填)。
- **處理邏輯**：
  1. 檢查 `title` 是否為空。若為空，透過 `flash()` 顯示錯誤。
  2. 呼叫 `TaskModel.create(title)`。
- **輸出**：重導向回 `GET /`。

### `POST /tasks/<id>/toggle`
- **輸入**：URL 變數 `id`。
- **處理邏輯**：呼叫 `TaskModel.toggle_status(id)`。
- **輸出**：重導向回 `GET /`。

### `GET /tasks/<id>/edit`
- **輸入**：URL 變數 `id`。
- **處理邏輯**：呼叫 `TaskModel.get_by_id(id)`。若找不到任務，回傳 404 錯誤。
- **輸出**：渲染 `tasks/edit.html` 並傳入 `task` 變數。

### `POST /tasks/<id>/edit`
- **輸入**：URL 變數 `id`，表單欄位 `title`。
- **處理邏輯**：
  1. 檢查 `title` 是否為空。
  2. 呼叫 `TaskModel.update(id, title)`。
- **輸出**：重導向回 `GET /`。

### `POST /tasks/<id>/delete`
- **輸入**：URL 變數 `id`。
- **處理邏輯**：呼叫 `TaskModel.delete(id)`。
- **輸出**：重導向回 `GET /`。

## 3. Jinja2 模板清單

所有的模板將放於 `app/templates/` 目錄底下。

1. **`base.html`**：基礎模板。
   - 包含 `<head>` 區塊，引入 Bootstrap 5 CDN。
   - 顯示共用導覽列。
   - 顯示 Flask `flash()` 訊息的區塊。
   - 留有 `{% block content %}{% endblock %}` 供子頁面填入。
2. **`tasks/index.html`**：繼承自 `base.html`。
   - 顯示新增任務的輸入框與送出按鈕。
   - 顯示狀態過濾頁籤 (全部 / 未完成 / 已完成)。
   - 使用 `{% for task in tasks %}` 迴圈渲染任務清單，包含每個任務的完成核取框、編輯按鈕與刪除按鈕。
3. **`tasks/edit.html`**：繼承自 `base.html`。
   - 顯示修改任務名稱的表單與「儲存」、「取消」按鈕。

## 4. 路由骨架程式碼

路由的骨架定義將存放於 `app/routes/task.py`。我們將使用 Blueprint 命名為 `task_bp`。
