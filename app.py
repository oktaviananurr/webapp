import streamlit as st
from sqlalchemy import text

list_dosen_pembimbing = ['','Ir.Sri Pingit Wulandari,M.Si', 'Dr.Drs.Brodjol Sutijo Supri Ulama', 'Dr.Wahyu Wibowo,S.Si,M.Si']
list_co_pembimbing= ['', 'Fausania Hibatullah S.Stat.,M.Stat','Muhammad Alfian Nuriman, S.Stat' ]
list_penguji= ['Dra.Lucia Aridinanti,MS', 'Dwi Endah Kusrini,S.Si,M.Si', 'Dra.Destri Susilaningrum,M.Si', 'Iis Dewi Ratih,S.Si.,M.Si', 'Zakiatul Wildani,S.Si.,M.Sc', 'Dra.Sri Mumpuni Retnaningsih,MT', 'Mukti Ratna Dewi,S.Si.,M.Sc']


conn = st.connection("postgresql", type="sql", 
                     url="postgresql://oktaviana12002:qihNL1mB4AkH@ep-silent-lake-46622122.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, mahasiswa_name varchar,  dosen_pembimbing varchar, co_pembimbing char(25), \
                                                      penguji varchar, nrp text, ruang text, waktu time,  tanggal date);')
    session.execute(query)

st.write(
    f"""
    <style>
        .stApp {{
            background-color: #FFA500;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.header('JADWAL SEMINAR PROPOSAL PROYEK AKHIR MAHASISWA DEPARTEMEN STATISTIKA BISNIS FAKULTAS VOKASI ITS SEMESTER GASAL 2023/2024')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":

    search_input = st.text_input("Cari Nama Mahasiswa", "")

    query_str = f"SELECT * FROM schedule WHERE LOWER(mahasiswa_name) LIKE LOWER('%{search_input}%') OR LOWER(dosen_pembimbing) LIKE LOWER('%{search_input}%') OR LOWER(co_pembimbing) LIKE LOWER('%{search_input}%') ORDER By id;"
    data = conn.query(query_str, ttl="0").set_index('id')
    sst.dataframe(data.style.applymap(color_negative_red, subset=['mahasiswa_name', 'dosen_pembimbing', 'co_pembimbing', 'penguji', 'nrp', 'ruang', 'waktu', 'tanggal']))

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (mahasiswa_name, dosen_pembimbing, co_pembimbing, penguji, nrp, ruang, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':'[]', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        mahasiswa_name_lama = result["mahasiswa_name"]
        dosen_pembimbing_lama = result["dosen_pembimbing"]
        co_pembimbing_lama = result["co_pembimbing"]
        penguji_lama = result["penguji"]
        nrp_lama = result["nrp"]
        ruang_lama = result["ruang"]
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'a.n. {mahasiswa_name_lama}'):
            with st.form(f'data-{id}'):
                mahasiswa_name_baru =st.text_input("mahasiswa_name", mahasiswa_name_lama)
                dosen_pembimbing_baru = st.selectbox("dosen_pembimbing", list_dosen_pembimbing ,list_dosen_pembimbing.index(dosen_pembimbing_lama))
                co_pembimbing_baru = st.selectbox("co_pembimbing", list_co_pembimbing , list_co_pembimbing.index(co_pembimbing_lama))
                penguji_baru = st.multiselect("penguji", [penguji for penguji in list_penguji])
                nrp_baru = st.text_input("nrp", nrp_lama)
                ruang_baru = st.text_input("ruang",ruang_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE schedule \
                                          SET mahasiswa_name=:1,dosen_pembimbing=:2, co_pembimbing=:3, penguji=:4, \
                                          nrp=:5, ruang=:6, waktu=:7, tanggal=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':mahasiswa_name_baru, '2':dosen_pembimbing_baru, '3':co_pembimbing_baru, '4':str(penguji_baru), 
                                                    '5':nrp_baru, '6':ruang_baru, '7':waktu_baru, '8':tanggal_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
