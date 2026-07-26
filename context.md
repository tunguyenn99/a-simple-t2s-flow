# 🛒 Xóm E-Com — Global E-Commerce Data Analytics Context

> **Đề bài & Ngữ cảnh Dự án**: Lấy trực tiếp từ [Xóm Dataset — Schema E-Commerce](https://dataset.xomdata.com/datasets/schema/e_commerce).

---

## 📌 Tổng quan về Xóm E-Com
**Xóm E-Com** là sàn thương mại điện tử B2C hoạt động tại hơn 140 quốc gia, trải rộng 4 market chính:
- **US** (Bắc Mỹ)
- **EMEA** (Châu Âu, Trung Đông, Châu Phi)
- **APAC** (Châu Á - Thái Bình Dương)
- **LATAM** (Mỹ La-tinh)

Khác với Xóm Retail (cửa hàng vật lý), Xóm E-Com không có cửa hàng vật lý — toàn bộ giao dịch diễn ra qua Web & App, hàng được giao trực tiếp đến địa chỉ khách hàng thông qua các đối tác logistics.

---

## 🗄️ Dữ liệu Nguồn (Source Datasets)
Schema `e_commerce` gồm 4 bảng dữ liệu chính:

| Bảng | Dung lượng | Số cột | Mô tả |
| :--- | :--- | :--- | :--- |
| **`customer`** | 17.4K dòng | 11 cột | Thông tin phân khúc, giới tính, nghề nghiệp, địa chỉ khách hàng. |
| **`ecom_sales`** | 51.3K dòng | 11 cột | Giao dịch đơn hàng online, doanh thu, lợi nhuận, mức discount. |
| **`product`** | 28.4K dòng | 4 cột | Danh mục sản phẩm (Office Supplies, Furniture, Technology) & SKU. |
| **`region`** | 3.8K dòng | 8 cột | Thông tin địa lý quốc gia, thị trường (Market) và khu vực (Region). |

---

## 💼 Mô hình Kinh doanh (Business Model)
- **Doanh thu**: ~$2.3M USD / năm.
- **Gross Margin**: ~20% (thấp hơn retail do chi phí logistics + chính sách discount aggressive).
- **Catalog**: ~1,900 SKU thuộc 3 category lớn: *Office Supplies*, *Furniture*, *Technology*.
- **Phân khúc Khách hàng (Segments)**:
  - **Consumer** (Khách hàng cá nhân): Chiếm 60% tổng lượng đơn hàng.
  - **Corporate** (Khách hàng B2B): Chiếm 25%.
  - **Home Office** (Khách hàng SMB): Chiếm 15%.

---

## 🚨 Bài toán Kinh doanh & Pain Points
1. **Discount Cannibalization**: Marketing chạy discount rất mạnh (20–80%) để kéo volume nhưng chưa đo lường tác động đến lợi nhuận. Có nhiều đơn hàng discount đến 80% dẫn tới profit bị âm.
2. **Segment Profitability**: Ban lãnh đạo nghi vấn Corporate là "cash cow", nhưng CFO chưa bao giờ xây P&L chi tiết theo từng segment.
3. **Geographic Expansion**: Xóm E-Com muốn mở rộng thêm market, cần xác định market nào đang tăng trưởng tốt và market nào đang bão hòa.
4. **Customer LTV Gap**: Tỷ lệ quay lại mua hàng thấp — phần lớn khách hàng chỉ mua 1 lần rồi ngưng tương tác.

---

## 🎯 Trách nhiệm của Business Analyst / Data Engineer
Bạn nhận yêu cầu ad-hoc truy vấn & phân tích từ các Trưởng bộ phận (**Head of Growth**, **Head of Finance**, **CMO**, **Head of Merchandising**). Dataset đã được tính sẵn doanh thu và margin trên từng dòng đơn hàng, do đó trọng tâm là xây dựng **Kho dữ liệu DuckDB (Medallion Architecture)**, chạy pipeline chuyển đổi dữ liệu với **dbt**, tích hợp **Text-to-SQL Engine**, và xuất các **Executive Dashboards**.

---

## 🔍 Danh sách Câu hỏi Truy vấn Ad-hoc (Từ Cơ bản đến Nâng cao)

### 🔹 Cơ bản (Basic Level)
1. **Q1: Tổng doanh thu và lợi nhuận** (`aggregate`)
2. **Q2: Doanh thu theo phân khúc khách hàng** (`group-by`, `order-by`)
3. **Q3: Top 10 sản phẩm bán nhiều nhất** (`join`, `group-by`, `top-n`)
4. **Q4: Phân bố số lượng khách hàng theo Giới tính × Nghề nghiệp** (`group-by`)
5. **Q5: Tỷ lệ Discount trung bình theo Danh mục sản phẩm** (`join`, `group-by`, `avg`)

### 🔸 Trung cấp (Intermediate Level)
6. **Q6: Tỷ lệ Profit Margin theo Thị trường (Market)** (`join`, `group-by`, `having`)
7. **Q7: Thống kê số lượng đơn hàng bị lỗ theo Phân khúc** (`case-when`, `conditional-count`)
8. **Q8: Nhận diện khách hàng VIP có nguy cơ Churn** (`subquery`, `date-arithmetic`, `ranking`)
9. **Q9: So sánh hành vi Mua chéo (Cross-sell) Consumer vs Corporate** (`pivot`, `case-when`, `share-of-total`)
10. **Q10: Top 15 quốc gia có doanh thu cao nhất** (`join`, `count-distinct`, `top-n`)

### 🚀 Nâng cao (Advanced Level)
11. **Q11: Tăng trưởng doanh thu YoY theo từng tháng** (`cte`, `window`, `lag`)
12. **Q12: Top 3 sản phẩm lợi nhuận cao nhất trong mỗi Category** (`window`, `partition-by`, `row-number`)
13. **Q13: Khách hàng mua sắm xuyên thị trường (Cross-market)** (`window`, `first-value`, `partition-by`)
14. **Q14: Phân nhóm khách hàng theo mô hình RFM** (`ntile`, `rfm`, `cte`)
15. **Q15: Phân tích giỏ hàng — Các sản phẩm thường được mua cùng nhau** (`self-join`, `market-basket`, `cte`)