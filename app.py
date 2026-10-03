import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)
st.image("logo.jpg")
st.title("💰 Máy tính lãi suất tiết kiệm")
st.caption("Tính tiền lãi theo lãi đơn hoặc lãi kép")

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📌 Thông tin khoản gửi")
so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)
ky_han = st.number_input("Kỳ hạn (tháng)", min_value=1, value=12, step=1)
lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)
hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
)
loai_lai = st.radio("Loại lãi", ["Lãi đơn", "Lãi kép"], horizontal=True)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", use_container_width=True):
    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được âm.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_thang = lai_suat / 100 / 12

    # Số tháng của kỳ hạn
    so_thang = int(ky_han)

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":
        # Tổng lãi: P * r * t
        tong_lai = so_tien * (lai_suat / 100) * (so_thang / 12)

        # Lãi định kỳ
        if hinh_thuc_nhan_lai == "Hàng tháng":
            lai_dinh_ky = tong_lai / so_thang
        elif hinh_thuc_nhan_lai == "Hàng quý":
            so_quy = so_thang / 3
            lai_dinh_ky = tong_lai / so_quy if so_quy > 0 else 0
        else:
            lai_dinh_ky = tong_lai

        tong_tien = so_tien + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:
        # Số lần nhập lãi vào gốc
        if hinh_thuc_nhan_lai == "Hàng tháng":
            so_ky = so_thang
            lai_suat_ky = lai_suat_thang
        elif hinh_thuc_nhan_lai == "Hàng quý":
            so_ky = so_thang // 3
            lai_suat_ky = lai_suat_thang * 3
        else:
            # Cuối kỳ: nhập lãi vào gốc một lần
            so_ky = 1
            lai_suat_ky = lai_suat / 100 * (so_thang / 12)

        # Giá trị cuối cùng
        tong_tien = so_tien * ((1 + lai_suat_ky) ** so_ky)
        tong_lai = tong_tien - so_tien

        # Lãi của kỳ đầu tiên
        lai_dinh_ky = so_tien * lai_suat_ky

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán thành công!")
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💵 Tiền lãi định kỳ", f"{lai_dinh_ky:,.0f} VNĐ")

    with col2:
        st.metric("📈 Tổng tiền lãi", f"{tong_lai:,.0f} VNĐ")

    st.metric("💰 Tổng tiền nhận được", f"{tong_tien:,.0f} VNĐ")

    # =========================
    # CHI TIẾT
    # =========================
    st.divider()
    st.subheader("📋 Chi tiết khoản gửi")

    st.write(f"**Số tiền gốc:** {so_tien:,.0f} VNĐ")
    st.write(f"**Kỳ hạn:** {so_thang} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Phương pháp:** {loai_lai}")

    # =========================
    # BẢNG MINH HỌA
    # =========================
    if loai_lai == "Lãi kép":
        st.divider()
        st.subheader("📅 Diễn biến tiền gửi")

        du_no = so_tien
        du_lieu = []

        if hinh_thuc_nhan_lai == "Hàng tháng":
            for thang in range(1, so_thang + 1):
                tien_lai = du_no * lai_suat_thang
                du_no += tien_lai
                du_lieu.append({
                    "Kỳ": f"Tháng {thang}",
                    "Tiền lãi": f"{tien_lai:,.0f} VNĐ",
                    "Số dư": f"{du_no:,.0f} VNĐ"
                })
        elif hinh_thuc_nhan_lai == "Hàng quý":
            lai_suat_quy = lai_suat_thang * 3
            so_quy = so_thang // 3
            for quy in range(1, so_quy + 1):
                tien_lai = du_no * lai_suat_quy
                du_no += tien_lai
                du_lieu.append({
                    "Kỳ": f"Quý {quy}",
                    "Tiền lãi": f"{tien_lai:,.0f} VNĐ",
                    "Số dư": f"{du_no:,.0f} VNĐ"
                })
        else:
            du_lieu.append({
                "Kỳ": "Cuối kỳ",
                "Tiền lãi": f"{tong_lai:,.0f} VNĐ",
                "Số dư": f"{tong_tien:,.0f} VNĐ"
            })

        st.table(du_lieu)

# =========================
# FOOTER
# =========================
st.divider()
st.caption(
    "💡 Lưu ý: Đây là công cụ tính toán mô phỏng. "
    "Lãi suất thực tế của ngân hàng có thể áp dụng các quy định khác nhau "
    "về cách tính và làm tròn tiền lãi."
)
