# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11xxxxxx  
**系級：** 資管系大一  
**姓名：** 王小明  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| l1 (in load_proc) | 檔案或資料來源讀入後的資料列集合（list of records/lines） | loaded_lines 或 records |
| d2 (in main) | 主程式保存的資料物件（單筆或整批資料的 dict/list），供後續處理使用 | main_data 或 dataset |
| c_res (in check) | 檢查/驗證函式的回傳結果（通常為 bool 或錯誤/合格訊息） | check_result 或 validation_result |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：難懂的變數名稱（如 l1, d2, c_res）** — 造成可讀性差、維護者難以理解變數用途與資料型態。  
- **Q2：大型函式/複合責任（Single Function 做太多事）** — 測試與重構困難，違反單一職責原則。  
- **Q3：缺乏輸入/錯誤處理 (no error handling)** — 遇到壞資料或 I/O 例外容易崩潰，缺乏恢復策略。  
- **Q4：缺少文件與型別資訊（no docstrings/type hints）** — 無法快速知道函式的輸入/輸出型態與前置條件。  
- **Q5：隱性全域狀態或副作用（global state / mutating inputs）** — 測試困難且容易產生難追蹤的 bug。  
- **Q6：重複程式碼 / 魔數（duplicated code / magic numbers）** — 維護成本高，修改時容易遺漏更新。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 
1. 請在 VSCode 中開啟 `legacy_lib.py`。
2. 使用 GitHub Copilot Chat 功能分析程式碼。
3. 在 `Answer.MD` 中完成「變數與邏輯對照表」，找出神祕變數 `l1`, `d2`, `c_res` 的真實意義。
4. 診斷出 **5 個以上** 的「代碼壞味道 (Code Smells)」，並說明為何這些設計會造成維護困難。
請以以下格式回答並且修改legacy_lib.py
| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|

Prompt B： 

Prompt C：
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

2. 發現的問題： (範例：AI 漏掉了 exit 時要印出分類統計的功能)

3. 修正的對話： (範例：我告訴它「請在結束前迴圈遍歷 JSON 資料並計算分類總額」)

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log

```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "XXX",
    "isbn": "XXX",
    "status": "XXX"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
# 請在此處貼上 git log 內容
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/Winnie-0917/B11208058-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
