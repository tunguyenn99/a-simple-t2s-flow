# Xóm E-Com
Thương mại điện tử B2C đa khu vực

## Dữ liệu nguồn
- `customer` (e_commerce): 17.4K dòng, 11 cột
- `ecom_sales` (e_commerce): 51.3K dòng, 11 cột
- `product` (e_commerce): 28.4K dòng, 4 cột
- `region` (e_commerce): 3.8K dòng, 8 cột

## Giới thiệu
**Xóm E-Com** là sàn thương mại điện tử hoạt động tại hơn 140 quốc gia, trải rộng 4 market chính:
- US
- EMEA
- APAC
- LATAM

Không có cửa hàng vật lý; toàn bộ giao dịch qua web và app, ship trực tiếp đến khách hàng bằng đối tác logistics.

## Business model
- Doanh thu ~2.3M USD/năm
- Gross margin ~20% (thấp hơn retail do phí logistics và chính sách discount mạnh)
- Catalog: 3 category chính - Office Supplies, Furniture, Technology
- SKU khoảng 1.900
- Customer segment:
  - Consumer (cá nhân): 60% volume
  - Corporate (B2B): 25%
  - Home Office (SMB): 15%

## Pain points
1. Discount cannibalization
   - Marketing chạy discount mạnh (20-80%) để kéo volume
   - Thiếu đo lường ảnh hưởng đến profit
   - Có đơn hàng discount 80% dẫn tới profit âm
2. Segment profitability
   - C-suite nghi Corporate là cash cow
   - CFO chưa xây P&L theo segment
3. Geographic expansion
   - Cần biết thị trường hiện tại đang tăng trưởng hay bão hoà
4. Customer LTV gap
   - Phần lớn khách mua 1 lần rồi không quay lại

## Vai trò analyst
- Bạn là Business Analyst
- Nhận yêu cầu từ:
  - Head of Growth
  - Head of Finance
  - CMO
  - Head of Merchandising
- Khác với retail, dataset đã có sẵn doanh thu và margin ở mỗi dòng đơn hàng, nên trọng tâm là truy vấn và phân tích nhanh.

## Yêu cầu ad-hoc
Truy vấn nhanh từ Leader/Stake Holder. Độ khó tăng dần từ cơ bản đến nâng cao.

### Cơ bản
1. Q1: Tổng doanh thu và profit
   - Kỹ thuật: aggregate
2. Q2: Doanh thu theo segment
   - Kỹ thuật: group-by, order-by
3. Q3: Top 10 sản phẩm bán nhiều nhất
   - Kỹ thuật: join, group-by, top-n
4. Q4: Số khách theo giới tính × nghề nghiệp
   - Kỹ thuật: group-by
5. Q5: Mức discount trung bình theo category
   - Kỹ thuật: join, group-by, avg

### Trung cấp
6. Q6: Profit margin theo market
   - Kỹ thuật: join, group-by, having
7. Q7: Đơn lỗ theo segment
   - Kỹ thuật: case-when, conditional-count
8. Q8: Khách VIP có nguy cơ churn
   - Kỹ thuật: subquery, date-arithmetic, ranking
9. Q9: Cross-sell Consumer vs Corporate
   - Kỹ thuật: pivot, case-when, share-of-total
10. Q10: Top 15 quốc gia theo doanh thu
   - Kỹ thuật: join, count-distinct, top-n

### Nâng cao
11. Q11: Tăng trưởng doanh thu YoY theo tháng
    - Kỹ thuật: cte, window, lag
12. Q12: Top 3 sản phẩm profit nhất mỗi category
    - Kỹ thuật: window, partition-by, row-number
13. Q13: Khách mua cross-market
    - Kỹ thuật: window, first-value, partition-by
14. Q14: Phân khúc khách theo RFM
    - Kỹ thuật: ntile, rfm, cte
15. Q15: Sản phẩm hay mua cùng
    - Kỹ thuật: self-join, market-basket, cte