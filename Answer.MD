# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11208058
**系級：** 資管系大三 
**姓名：** 沈晨利

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| l1 | 讀取的原始檔案內容行列表| lines |
| d2 | 儲存圖書資料的記憶體清單 | books |
| c_res | 檢查 ISBN 是否已存在於資料庫的檢查函數 | check_isbn_exists |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：全局變數使用 (books): 使用全域變數導致資料狀態不透明，若程式規模擴大，函數間的副作用將難以追蹤。**
- **Q2：檔案操作缺乏上下文管理: 直接使用 open() 與 close() 若發生例外，檔案控制代碼 (file handle) 可能無法正常釋放。**  
- **Q3：魔法字串 (Magic Strings/Separators): @@ 與 ## 等分隔符直接散落在邏輯中，未來若資料格式改變，必須在多處修改，極易出錯。** 
- **Q4：責任過載 (God Function): main() 函數包辦了輸入讀取、指令解析、資料處理與存儲，違反了單一職責原則。**  
- **Q5：缺乏例外處理 (Robustness): 若 lib_data.txt 內容格式不正確，p[1].split("##") 將觸發 IndexError 導致程式崩潰** 
- **Q6：資料結構模糊: 直接使用字典 {'t': ..., 'i': ..., 's': ...} 存取屬性，缺乏明確的資料定義，開發者難以得知欄位實際含義（容易打錯字）。**

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
1. 目標： 撰寫 `modern_library.py`。

    - 模組化： 將功能拆解為類別 (Class) 或多個函式 (Function)。
    - 格式升級： 捨棄原本的 `txt` 混亂分割格式，改用標準 `json` 格式儲存。
    - 強健性： 增加對使用者輸入與檔案讀取的錯誤處理 (Try-Except)。
    - 優化： 修正原程式每次新增資料都要開啟磁碟寫入的低效率行為。    
並根據代碼壞味道 (Code Smells) 診斷來更改代碼

Prompt C：
目標：優化 `modern_library.py` 的指令解析 (Parsing) 與防呆機制。
目前問題：當使用者輸入格式稍微錯誤（例如 `add/tsdsa`，指令與資料間忘記加空白鍵）時，系統會直接將整串視為未知指令並跳出 `Unknown Command`，缺乏明確的除錯指引。
要求：請修改 `main()` 迴圈中的字串切割與條件判斷邏輯。當指令缺少必要參數、或分隔符號使用錯誤時，請正確攔截，並印出具體的提示訊息（例如：`Format Error: Please provide Title/ISBN/Status`），以提升系統的容錯性與整體使用者體驗。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？
回答： 有的。在將資料儲存格式從 txt 改寫為 json 的過程中，AI 寫的檔案寫入邏輯存在編碼設定上的遺漏。雖然程式在終端機運作時一切正常、沒有報錯，但當我實際打開輸出的 books.json 檔案檢查時，發現裡面的中文書名全部變成了不可讀的 Unicode 亂碼。我直接將檔案裡儲存的亂碼片段複製貼給 AI，詢問為何中文無法正常寫入，並請它提供修正方法。

2. 發現的問題： (範例：AI 漏掉了 exit 時要印出分類統計的功能)
 發現了JSON 中文編碼異常 (Encoding Issue)：
 AI 在撰寫 save_data 函式時，使用了標準的 json.dump(data, f)，但漏掉了處理非英文字元的關鍵參數。這導致當我新增像「深入淺出Python」這類含有中文的資料並執行 exit 存檔後，books.json 裡的 title 變成了一大串像是 \u6df1\u5165\u6dfa\u51fa 的 Unicode 跳脫字元。這雖然符合 JSON 規範，但完全喪失了人類可讀性，也會造成後續系統除錯的困難。

3. 修正的對話： (範例：我告訴它「請在結束前迴圈遍歷 JSON 資料並計算分類總額」)
Prompt： 我執行 exit 存檔後，打開 books.json 發現中文書名都變成了 \u6df1\u5165... 這種奇怪的編碼，要怎麼修改才能讓檔案正常顯示中文？
AI 隨即解釋，這是因為 Python 的 json.dump() 預設會確保所有輸出的字元都是 ASCII，遇到非 ASCII 字元（如中文）就會自動進行 Unicode 轉義。AI 接著提供了修正後的程式碼，指示我在寫入時必須加上 ensure_ascii=False 參數，同時確保 open() 函式有明確指定 encoding="utf-8"（例如：json.dump(..., ensure_ascii=False, indent=4)）。修改後再次測試，JSON 檔案終於能完美呈現正確的繁體中文了。
---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
=== 圖書管理系統 v1.0 (Modernized) ===
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
    {
        "title": "深入淺出Python",
        "isbn": "978001",
        "status": "available"
    },
    {
        "title": "資料結構理論",
        "isbn": "978002",
        "status": "borrowed"
    },
    {
        "title": "演算法實作",
        "isbn": "978003",
        "status": "available"
    }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
183db1a (HEAD -> main) .
13d9151 change Answer.MD
98081c1 add modern_library.py
19c59bf change variable name
f3ca36a first commit
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/Winnie-0917/B11208058-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
