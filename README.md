# 📊 ChurnX AI - Hệ Thống Dự Đoán & Phân Tích Rời Bỏ Của Khách Hàng (Customer Churn Prediction)

**ChurnX AI** là một giải pháp phân tích và dự báo tỷ lệ rời bỏ của khách hàng (Customer Churn) toàn diện cấp doanh nghiệp. Hệ thống được xây dựng trên sự kết hợp giữa mô hình học máy **XGBoost Classifier** tối ưu, backend **FastAPI** hiệu năng cao, và giao diện bảng điều khiển (Dashboard) trực quan, hiện đại bằng **Vue 3 + Vite + TailwindCSS 4**.

Dự án này nằm trong môn học **Khai phá dữ liệu (KPDL)** - Học kỳ 2, Năm 3.

---

## 🚀 Các Tính Năng Cốt Lõi

### 1. Phân Tích Dữ Liệu Lớn & Phân Khúc Khách Hàng (EDA & RFM)

- **Khám phá dữ liệu (EDA)**: Phân tích trực quan các yếu tố tác động trực tiếp đến hành vi rời bỏ (Churn) của khách hàng thương mại điện tử như: thâm niên (Tenure), khiếu nại (Complain), mức độ hài lòng (SatisfactionScore),...

### 2. Mô Hình Dự Đoán Học Máy (XGBoost Engine)

- Sử dụng mô hình **XGBoost Classifier** đạt độ chính xác cao trên tập dữ liệu thương mại điện tử.
- Dữ liệu đầu vào được tiền xử lý bài bản qua các bước: xử lý giá trị khuyết thiếu bằng **KNN Imputer**, mã hóa một nóng (**One-Hot Encoding**), và chuẩn hóa dữ liệu số bằng **MinMaxScaler** trước khi đưa vào mô hình.

### 3. API Backend Hiệu Năng Cao (FastAPI)

- **Dự đoán thời gian thực**: Cung cấp endpoint `/predict` xử lý dữ liệu khách hàng đơn lẻ nhanh chóng.
- **Xác định các yếu tố ảnh hưởng**: Phân tích độ đóng góp đặc trưng (Feature Importances) của mô hình để trả về top 5 lý do chính làm tăng hoặc giảm rủi ro khách hàng rời đi.

### 4. Giao Diện Bảng Điều Khiển Doanh Nghiệp (ChurnX AI Frontend)

- **Dashboard trực quan**: Theo dõi các chỉ số rủi ro ròng, phân khúc khách hàng, và trực quan hóa dữ liệu trực quan.
- **Dự đoán đơn lẻ (Single Predict)**: Giao diện nhập thông tin chi tiết của một khách hàng và nhận kết quả phân loại rủi ro (Low / Medium / High Risk) ngay lập tức.
- **Dự đoán hàng loạt (Batch Upload)**: Hỗ trợ kéo thả/tải lên file danh sách khách hàng để phân tích rủi ro hàng loạt nhanh chóng.
- **Đề xuất Retention thông minh**: Tích hợp gợi ý các chiến dịch ưu đãi, dịch vụ chăm sóc khách hàng dựa trên hành vi và đặc điểm rủi ro cụ thể của từng người.

---

## 📂 Cấu Trúc Dự Án

```text
churn-prediction/
├── backend/                        # FastAPI Backend & Data Analysis
│   ├── Data_Cleaning_and_Analysis.ipynb # File Jupyter Notebook phân tích EDA, RFM và huấn luyện XGBoost
│   ├── E Commerce Dataset.csv      # File dataset gốc (Excel/ZIP format)
│   ├── E_Comm_Cleaned.csv          # Dataset sau bước làm sạch cơ bản
│   ├── E_Comm_Cleaned_with_RFM.csv # Dataset đã làm sạch và tích hợp phân khúc RFM
│   ├── main.py                     # API Server FastAPI (chứa logic chuẩn hóa đầu vào & dự đoán)
│   ├── requirements.txt            # Thư viện Python cần thiết
│   └── test_samples.json           # 4 mẫu dữ liệu chuẩn phục vụ kiểm thử nhanh
├── churnx-ai/                      # Vue 3 Frontend (Vite + TailwindCSS 4)
│   ├── src/
│   │   ├── components/             # Các Component giao diện (Dashboard, Sidebar, TopNav, BatchUpload,...)
│   │   ├── App.vue                 # Luồng ứng dụng chính
│   │   └── index.css               # Hệ thống định kiểu toàn cục (TailwindCSS)
│   ├── package.json                # Dependencies của Frontend
│   └── vite.config.ts              # Cấu hình Vite bundler
├── xgboost_model.json              # File lưu trữ mô hình XGBoost đã huấn luyện xong
└── README.md                       # Tài liệu hướng dẫn dự án (File này)
```

---

## 🛠️ Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Khởi Chạy Backend (FastAPI Server)

Yêu cầu máy tính cài đặt sẵn **Python 3.8+**.

Khởi chạy terminal và di chuyển vào thư mục `backend`:

```bash
cd backend
```

Tạo môi trường ảo (Khuyến khích):

```bash
python -m venv venv
# Kích hoạt trên Windows (PowerShell):
.\venv\Scripts\Activate
```

Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

Khởi động API Server bằng Uvicorn:

```bash
uvicorn main:app --reload
```

API lúc này sẽ hoạt động tại địa chỉ: `http://127.0.0.1:8000`

---

### 2. Khởi Chạy Frontend (ChurnX AI Dashboard)

Yêu cầu máy tính cài đặt sẵn **Node.js** và quản lý gói **npm** hoặc **yarn**.

Mở một terminal mới ở thư mục gốc dự án và di chuyển vào thư mục `churnx-ai`:

```bash
cd churnx-ai
```

Cài đặt các gói tài nguyên Frontend:

```bash
npm install
# hoặc nếu dùng yarn:
yarn install
```

Khởi chạy máy chủ phát triển (Development Server):

```bash
npm run dev
# hoặc:
yarn dev
```

Giao diện ChurnX AI sẽ hoạt động tại địa chỉ: `http://localhost:3000` (hoặc cổng được hiển thị trong terminal).

---

## 🧪 Kiểm Thử Nhanh (API Testing)

Bạn có thể sử dụng file mẫu [test_samples.json](file:///d:/Documents/BaiTap/Ki2Nam3/KPDL/churn-prediction/churn-prediction/backend/test_samples.json) được cung cấp trong thư mục `backend` để gửi POST request đến API `http://127.0.0.1:8000/predict` phục vụ kiểm tra tính chính xác của mô hình:

- **Mẫu 1 & Mẫu 2**: Rủi ro cực cao (**High Risk / Churn = 1**). Phù hợp để kiểm tra khả năng bắt lỗi rủi ro khách hàng rời đi sớm và có nhiều khiếu nại.
- **Mẫu 3 & Mẫu 4**: Rủi ro thấp (**Low Risk / Churn = 0**). Đại diện cho các khách hàng trung thành, chi tiêu tốt, mức độ hài lòng cao.

Ví dụ Payload cho khách hàng rủi ro cao (Mẫu 1):

```json
{
  "Tenure": 4.0,
  "CityTier": 3.0,
  "WarehouseToHome": 6.0,
  "PreferredPaymentMode": "Debit Card",
  "Gender": "Female",
  "HourSpendOnApp": 3.0,
  "NumberOfDeviceRegistered": 3.0,
  "PreferedOrderCat": "Laptop & Accessory",
  "SatisfactionScore": 2.0,
  "MaritalStatus": "Single",
  "NumberOfAddress": 9.0,
  "Complain": true,
  "OrderAmountHikeFromlastYear": 11.0,
  "CouponUsed": 1.0,
  "OrderCount": 1.0,
  "DaySinceLastOrder": 5.0,
  "CashbackAmount": 160.0,
  "PreferredLoginDevice": "Mobile Phone"
}
```

---

## 📈 Hiệu Năng Mô Hình

- **XGBoost Classifier** là mô hình có độ cân bằng và tổng thể hiệu suất tốt nhất trên tập dữ liệu Churn Prediction này sau khi được áp dụng SMOTE để giải quyết vấn đề mất cân bằng lớp.
- Chi tiết quá trình xử lý dữ liệu và huấn luyện so sánh giữa các mô hình (Logistic Regression, Decision Tree, Random Forest, XGBoost) được ghi lại đầy đủ và minh bạch trong file [Data_Cleaning_and_Analysis.ipynb](file:///d:/Documents/BaiTap/Ki2Nam3/KPDL/churn-prediction/churn-prediction/backend/Data_Cleaning_and_Analysis.ipynb).
