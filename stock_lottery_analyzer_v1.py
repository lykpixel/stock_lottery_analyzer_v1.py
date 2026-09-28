fromO streamlit as st
import pandas as pd
from io import BBytesIO
st.set_page_config(
    page_title="Stock Lottery Analyzer v1",
    page_icon="🎯",
    layout="wide",
)

# ============================================================
# MOBILE RESPONSIVE UI
# ============================================================

st.markdown("""
<style>

/* ---------- Global ---------- */

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

h1 {
    font-size: 1.65rem !important;
    margin-bottom: 0.25rem !important;
}

h2 {
    font-size: 1.3rem !important;
}

h3 {
    font-size: 1.1rem !important;
}

p, label, div {
    font-size: 0.95rem;
}


/* ---------- Metrics ---------- */

[data-testid="stMetric"] {
    padding: 0.45rem 0.55rem;
}

[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.25rem !important;
}


/* ---------- Selectbox ---------- */

[data-testid="stSelectbox"] {
    margin-bottom: 0.25rem;
}


/* ---------- Tables ---------- */

[data-testid="stDataFrame"] {
    width: 100%;
}

/* ---------- Mobile ---------- */

@media (max-width: 768px) {

    .block-container {
        padding-top: 0.7rem;
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }

    h1 {
        font-size: 1.35rem !important;
    }

    h2 {
        font-size: 1.15rem !important;
    }

    h3 {
        font-size: 1rem !important;
    }

    p, label, div {
        font-size: 0.88rem;
    }

    [data-testid="stMetric"] {
        padding: 0.3rem 0.4rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.05rem !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
    }

    /* ลดช่องว่างระหว่าง component */
    [data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# STOCK LOTTERY ANALYZER v1
# DATA ENGINE
# ============================================================

COLUMNS = [
    "date",
    "market",
    "session",
    "three_digit",
    "two_digit_top",
    "two_digit_bottom",
    "source",
    "verified",
]

MARKETS = {
    "A": "นิเคอิ",
    "B": "หุ้นไทย",
    "C": "ฮั่งเส็ง",
}

SESSIONS = {
    "AM": "เช้า",
    "PM": "บ่าย",
}

STATUS = [
    "VERIFIED",
    "CONFLICT",
    "NEW",
    "UNVERIFIED",
]

# ============================================================
# INITIAL DATA
# ============================================================

INITIAL_ROWS = [
    ["2026-09-25","A","AM","758","58","59","raakaadee","UNVERIFIED"],
    ["2026-09-24","A","AM","115","15","20","raakaadee","UNVERIFIED"],
    ["2026-09-18","A","AM","069","69","44","raakaadee","UNVERIFIED"],
    ["2026-09-17","A","AM","976","76","76","raakaadee","UNVERIFIED"],
    ["2026-09-16","A","AM","682","82","28","raakaadee","UNVERIFIED"],
    ["2026-09-15","A","AM","520","20","21","raakaadee","UNVERIFIED"],
    ["2026-09-11","A","AM","935","35","60","raakaadee","UNVERIFIED"],
    ["2026-09-10","A","AM","800","00","78","raakaadee","UNVERIFIED"],
    ["2026-09-09","A","AM","769","69","36","raakaadee","UNVERIFIED"],
    ["2026-09-04","A","AM","226","26","78","raakaadee","UNVERIFIED"],

    ["2026-09-25","A","PM","843","43","44","raakaadee","UNVERIFIED"],
    ["2026-09-24","A","PM","270","70","75","raakaadee","UNVERIFIED"],
    ["2026-09-18","A","PM","258","58","33","raakaadee","UNVERIFIED"],
    ["2026-09-17","A","PM","965","65","65","raakaadee","UNVERIFIED"],
    ["2026-09-16","A","PM","014","14","04","raakaadee","UNVERIFIED"],
    ["2026-09-15","A","PM","184","84","85","raakaadee","UNVERIFIED"],
    ["2026-09-11","A","PM","642","42","53","raakaadee","UNVERIFIED"],
    ["2026-09-10","A","PM","881","81","97","raakaadee","UNVERIFIED"],
    ["2026-09-03","A","PM","948","48","16","raakaadee","UNVERIFIED"],
    ["2026-09-02","A","PM","309","09","25","raakaadee","UNVERIFIED"],

    ["2026-09-25","B","AM","358","58","00","huaysad","VERIFIED"],
    ["2026-09-24","B","AM","534","34","36","huaysad","VERIFIED"],
    ["2026-09-23","B","AM","404","04","40","huaysad","VERIFIED"],
    ["2026-09-22","B","AM","345","45","42","huaysad","VERIFIED"],
    ["2026-09-21","B","AM","322","22","07","huaysad","VERIFIED"],
    ["2026-09-18","B","AM","036","36","02","huaysad","VERIFIED"],
    ["2026-09-17","B","AM","166","66","93","huaysad","VERIFIED"],
    ["2026-09-16","B","AM","169","69","03","huaysad","VERIFIED"],
    ["2026-09-15","B","AM","050","50","57","huaysad","VERIFIED"],
    ["2026-09-14","B","AM","317","17","35","huaysad","VERIFIED"],

    ["2026-09-25","B","PM","163","","05","lotto2news","UNVERIFIED"],
    ["2026-09-24","B","PM","658","","12","lotto2news","UNVERIFIED"],
    ["2026-09-23","B","PM","170","","26","lotto2news","UNVERIFIED"],
    ["2026-09-22","B","PM","044","","41","lotto2news","UNVERIFIED"],
    ["2026-09-21","B","PM","803","","88","lotto2news","UNVERIFIED"],
    ["2026-09-18","B","PM","615","","81","lotto2news","UNVERIFIED"],
    ["2026-09-17","B","PM","734","","61","lotto2news","UNVERIFIED"],
    ["2026-09-16","B","PM","673","","93","lotto2news","UNVERIFIED"],
    ["2026-09-15","B","PM","666","","41","lotto2news","UNVERIFIED"],
    ["2026-09-14","B","PM","707","","45","lotto2news","UNVERIFIED"],

    ["2026-09-25","C","AM","319","","94","lotto2news","UNVERIFIED"],
    ["2026-09-24","C","AM","475","","37","lotto2news","UNVERIFIED"],
    ["2026-09-23","C","AM","604","","71","lotto2news","UNVERIFIED"],
    ["2026-09-22","C","AM","175","","04","lotto2news","UNVERIFIED"],
    ["2026-09-21","C","AM","158","","80","lotto2news","UNVERIFIED"],
    ["2026-09-18","C","AM","884","","55","lotto2news","UNVERIFIED"],
    ["2026-09-17","C","AM","346","","32","lotto2news","UNVERIFIED"],
    ["2026-09-16","C","AM","735","","11","lotto2news","UNVERIFIED"],
    ["2026-09-15","C","AM","945","","15","lotto2news","UNVERIFIED"],
    ["2026-09-14","C","AM","311","","48","lotto2news","UNVERIFIED"],

    ["2026-09-25","C","PM","009","","04","punlekded","UNVERIFIED"],
    ["2026-09-24","C","PM","113","","99","punlekded","UNVERIFIED"],
    ["2026-09-23","C","PM","412","","63","punlekded","UNVERIFIED"],
    ["2026-09-22","C","PM","775","","04","punlekded","UNVERIFIED"],
    ["2026-09-21","C","PM","271","","93","punlekded","UNVERIFIED"],
    ["2026-09-18","C","PM","078","","49","punlekded","UNVERIFIED"],
    ["2026-09-17","C","PM","429","","49","punlekded","UNVERIFIED"],
    ["2026-09-16","C","PM","378","","54","punlekded","UNVERIFIED"],
    ["2026-09-15","C","PM","724","","36","punlekded","UNVERIFIED"],
    ["2026-09-14","C","PM","760","","97","punlekded","UNVERIFIED"],
]

# ============================================================
# NORMALIZE
# ============================================================

def normalize_df(df):
    df = df.copy()

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLUMNS]

    for col in COLUMNS:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df["market"] = df["market"].str.upper()
    df["session"] = df["session"].str.upper()
    df["verified"] = df["verified"].str.upper()

    return df


# ============================================================
# VALIDATION
# ============================================================

def validate_df(df):

    errors = []

    if df.empty:
        return ["ไม่มีข้อมูล"]

    for idx, row in df.iterrows():

        row_number = idx + 2

        # Date
        if not row["date"] or row["date"] == "NaT":
            errors.append(
                f"แถว {row_number}: วันที่ไม่ถูกต้อง"
            )

        # Market
        if row["market"] not in MARKETS:
            errors.append(
                f"แถว {row_number}: market ต้องเป็น A, B หรือ C"
            )

        # Session
        if row["session"] not in SESSIONS:
            errors.append(
                f"แถว {row_number}: session ต้องเป็น AM หรือ PM"
            )

        # Three digit
        value = row["three_digit"]

        if value:
            if len(value) != 3 or not value.isdigit():
                errors.append(
                    f"แถว {row_number}: 3 ตัวบนต้องเป็นตัวเลข 3 หลัก"
                )

        # Two digit
        for col in [
            "two_digit_top",
            "two_digit_bottom",
        ]:

            value = row[col]

            if value:
                if len(value) != 2 or not value.isdigit():
                    errors.append(
                        f"แถว {row_number}: {col} ต้องเป็นตัวเลข 2 หลัก"
                    )

        # Status
        if row["verified"] not in STATUS:
            errors.append(
                f"แถว {row_number}: verified ไม่ถูกต้อง"
            )

    return errors


# ============================================================
# DIGIT FREQUENCY
# ============================================================

def digit_frequency(series):

    counts = {
        str(i): 0
        for i in range(10)
    }

    for value in series:

        value = str(value)

        for digit in value:

            if digit.isdigit():
                counts[digit] += 1

    result = pd.DataFrame({
        "เลข": list(counts.keys()),
        "จำนวน": list(counts.values()),
    })

    return result.sort_values(
        "จำนวน",
        ascending=False
    )


# ============================================================
# POSITION FREQUENCY
# ============================================================

def position_frequency(series):

    positions = {
        "หลักร้อย": {},
        "หลักสิบ": {},
        "หลักหน่วย": {},
    }

    for value in series:

        value = str(value)

        if len(value) != 3:
            continue

        keys = [
            "หลักร้อย",
            "หลักสิบ",
            "หลักหน่วย",
        ]

        for key, digit in zip(keys, value):

            positions[key][digit] = (
                positions[key].get(digit, 0) + 1
            )

    tables = {}

    for key, data in positions.items():

        tables[key] = pd.DataFrame({
            "เลข": list(data.keys()),
            "จำนวน": list(data.values()),
        }).sort_values(
            "จำนวน",
            ascending=False
        )

    return tables


# ============================================================
# DUPLICATE CONTROL
# ============================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "date",
            "market",
            "session",
        ],
        keep="last",
    )

    removed = before - len(df)

    return df, removed


# ============================================================
# SESSION STATE
# ============================================================

if "dataset" not in st.session_state:

    st.session_state.dataset = normalize_df(
        pd.DataFrame(
            INITIAL_ROWS,
            columns=COLUMNS,
        )
    )


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Stock Lottery Analyzer v1")

st.caption(
    "Data Engine รองรับ A/B/C × AM/PM "
    "และออกแบบให้เพิ่มข้อมูลย้อนหลังได้เรื่อย ๆ"
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ ตัวกรอง")

    market = st.selectbox(
        "ตลาด",
        list(MARKETS.keys()),
        format_func=lambda x:
            f"{x} — {MARKETS[x]}",
    )

    session = st.selectbox(
        "รอบ",
        list(SESSIONS.keys()),
        format_func=lambda x:
            f"{x} — {SESSIONS[x]}",
    )

    window = st.selectbox(
        "ย้อนหลัง",
        [10, 20, 50, 100],
    )

    st.divider()

    st.caption("📊 ตลาดที่รองรับ")

    for m in MARKETS:
        st.caption(
            f"{m}-AM — {MARKETS[m]}เช้า  |  "
            f"{m}-PM — {MARKETS[m]}บ่าย"
        )

# ============================================================
# DATASET
# ============================================================

df = normalize_df(
    st.session_state.dataset
)


# ============================================================
# UPLOAD CSV
# ============================================================

st.subheader("📥 เพิ่มข้อมูล")

uploaded = st.file_uploader(
    "เลือก CSV เพื่อเพิ่มข้อมูล",
    type=["csv"],
)

if uploaded:
    try:
        incoming = pd.read_csv(
            uploaded,
            dtype=str,
        )
        incoming = normalize_df(
            incoming
        )
        errors = validate_df(
            incoming
        )
        if errors:
            st.error(
                "พบข้อมูลไม่ถูกต้อง"
            )
            for error in errors[:20]:
                st.write(
                    f"• {error}"
                )
        else:
            combined = pd.concat(
                [
                    st.session_state.dataset,
                    incoming,
                ],
                ignore_index=True,
            )
            combined, removed = (
                remove_duplicates(
                    combined
                )
            )
            st.session_state.dataset = (
                normalize_df(combined)
            )
            new_count = len(
                st.session_state.dataset
            )
            st.success(
                f"นำเข้า {len(incoming)} แถว "
                f"• ตัดข้อมูลซ้ำ {removed} แถว "
                f"• รวมทั้งหมด {new_count} แถว"
            )
            df = st.session_state.dataset.copy()
    except Exception as e:
        st.error(
            f"ไม่สามารถอ่านไฟล์ CSV ได้: {e}"
        )
        
# ============================================================
# FILTER
# ============================================================

df = normalize_df(
    st.session_state.dataset
)

filtered = df[
    (df["market"] == market)
    &
    (df["session"] == session)
].copy()

filtered = filtered.sort_values(
    "date",
    ascending=False,
)

recent = filtered.head(
    window
)

# ============================================================
# SUMMARY
# ============================================================

st.subheader(
    f"📊 {market} — "
    f"{MARKETS[market]} / "
    f"{SESSIONS[session]}"
)

total_verified = int(
    (
        filtered["verified"]
        == "VERIFIED"
    ).sum()
)

# Desktop: 4 columns
# Mobile: CSS จะช่วยให้แต่ละ Metric กระชับลง

c1, c2, c3, c4 = st.columns(
    4,
    gap="small",
)

with c1:
    st.metric(
        "ข้อมูลทั้งหมด",
        len(filtered),
    )

with c2:
    st.metric(
        f"ย้อนหลัง {window}",
        len(recent),
    )

with c3:
    st.metric(
        "VERIFIED",
        total_verified,
    )

with c4:
    st.metric(
        "รวมทุกตลาด",
        len(df),
    )


# ============================================================
# ANALYSIS
# ============================================================

if recent.empty:

    st.info(
        "ยังไม่มีข้อมูลของตลาด/รอบนี้"
    )

else:

    st.subheader(
        "🔢 วิเคราะห์ความถี่"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "3 ตัวบน",
            "2 ตัวบน",
            "2 ตัวล่าง",
        ]
    )

    # --------------------------------------------------------
    # 3 ตัวบน
    # --------------------------------------------------------

    with tab1:

        st.caption(
            f"ข้อมูลย้อนหลัง {len(recent)} งวด"
        )

        st.dataframe(
            digit_frequency(
                recent["three_digit"]
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.write(
            "### แยกตามตำแหน่ง"
        )

        position_tables = (
            position_frequency(
                recent["three_digit"]
            )
        )

        # ใช้ columns บน Desktop
        # และ CSS จะช่วยให้พื้นที่แสดงผลกระชับบน Mobile

        p1, p2, p3 = st.columns(
            3,
            gap="small",
        )

        with p1:

            st.caption("หลักร้อย")

            st.dataframe(
                position_tables["หลักร้อย"],
                use_container_width=True,
                hide_index=True,
            )

        with p2:

            st.caption("หลักสิบ")

            st.dataframe(
                position_tables["หลักสิบ"],
                use_container_width=True,
                hide_index=True,
            )

        with p3:

            st.caption("หลักหน่วย")

            st.dataframe(
                position_tables["หลักหน่วย"],
                use_container_width=True,
                hide_index=True,
            )

    # --------------------------------------------------------
    # 2 ตัวบน
    # --------------------------------------------------------

    with tab2:

        st.caption(
            f"ข้อมูลย้อนหลัง {len(recent)} งวด"
        )

        st.dataframe(
            digit_frequency(
                recent["two_digit_top"]
            ),
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # 2 ตัวล่าง
    # --------------------------------------------------------

    with tab3:

        st.caption(
            f"ข้อมูลย้อนหลัง {len(recent)} งวด"
        )

        st.dataframe(
            digit_frequency(
                recent["two_digit_bottom"]
            ),
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# RECENT RESULTS
# ============================================================

st.subheader("📋 ผลย้อนหลัง")

if recent.empty:

    st.info("ไม่มีข้อมูล")

else:

    st.dataframe(
        recent[
            [
                "date",
                "three_digit",
                "two_digit_top",
                "two_digit_bottom",
                "verified",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# SIX MARKET STATUS
# ============================================================

st.subheader(
    "🗂️ สถานะข้อมูล 6 กลุ่ม"
)

status_rows = []

for m in MARKETS:

    for s in SESSIONS:

        x = df[
            (df["market"] == m)
            &
            (df["session"] == s)
        ]

        status_rows.append({

            "กลุ่ม":
                f"{m}-{s}",

            "ตลาด":
                MARKETS[m],

            "รอบ":
                SESSIONS[s],

            "จำนวนงวด":
                len(x),

            "VERIFIED":
                int(
                    (
                        x["verified"]
                        == "VERIFIED"
                    ).sum()
                ),

            "CONFLICT":
                int(
                    (
                        x["verified"]
                        == "CONFLICT"
                    ).sum()
                ),

            "NEW":
                int(
                    (
                        x["verified"]
                        == "NEW"
                    ).sum()
                ),

            "ล่าสุด":
                x["date"].max()
                if not x.empty
                else "-",
        })

status_df = pd.DataFrame(
    status_rows
)

st.dataframe(
    status_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# DATA MANAGER
# ============================================================

st.subheader(
    "🛠️ จัดการข้อมูล"
)

with st.expander(
    "เปิดตารางข้อมูลทั้งหมด"
):

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="data_editor",
    )

    if st.button(
        "💾 บันทึกข้อมูล"
    ):

        edited = normalize_df(
            edited
        )

        errors = validate_df(
            edited
        )

        if errors:

            st.error(
                "ไม่สามารถบันทึกได้"
            )

            for error in errors[:20]:
                st.write(
                    f"• {error}"
                )

        else:

            edited, removed = (
                remove_duplicates(
                    edited
                )
            )

            st.session_state.dataset = (
                edited.sort_values(
                    "date",
                    ascending=False,
                )
            )

            st.success(
                f"บันทึกสำเร็จ "
                f"• ตัดข้อมูลซ้ำ {removed} แถว"
            )


# ============================================================
# EXPORT
# ============================================================

st.subheader(
    "📤 ส่งออก Dataset"
)

export_df = normalize_df(
    st.session_state.dataset
).sort_values(
    "date",
    ascending=False,
)

csv_data = export_df.to_csv(
    index=False,
    encoding="utf-8-sig",
)

st.download_button(
    "⬇️ ดาวน์โหลด Dataset CSV",
    data=csv_data,
    file_name="stock_lottery_v1_dataset.csv",
    mime="text/csv",
    use_container_width=True,
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "หมายเหตุ: โปรแกรมนี้ใช้สำหรับวิเคราะห์สถิติข้อมูลย้อนหลัง "
    "ไม่ใช่การรับประกันผลลัพธ์ในอนาคต"
)
