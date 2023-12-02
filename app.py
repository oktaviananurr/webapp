import streamlit as st
from sqlalchemy import text

list_mahasiswa_name = ['Ifayanti Rohmatul Hidayah', 'Adenia Lindi Mawarni', 'Nabila Aisha', 'Hanifah Inayah', 'Hemas Salsabila Trixie', 'Iid Aida Nafisah', 'Berlyana Andalusya', 'Fitria Anggraeni','Silmi Yudiane', 'Endah Sayekti Putri Pratiwy']
list_symptom = ['', 'Dra.Lucia Aridinanti,MS', 'Dr.Drs.Brodjol Sutijo Supri Ulama', 'Dr.Wahyu Wibowo,S.Si,M.Si', 'Dwi Endah Kusrini,S.Si,M.Si', 'Dra.Destri Susilaningrum,M.Si', 'Iis Dewi Ratih,S.Si.,M.Si', 'Zakiatul Wildani,S.Si.,M.Sc', 'Dra.Sri Mumpuni Retnaningsih,MT', 'Mukti Ratna Dewi,S.Si.,M.Sc', 'Muhammad Alfian Nuriman']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://oktaviana12002:qihNL1mB4AkH@ep-silent-lake-46622122.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, nama_mahasiswa varchar,  nrp varchar, dosen_pembimbing varchar, \
                                                      co_pempimbing varchar, penguji text, ruang text, tanggal date);')
    session.execute(query)

st.header('JADWAL SEMINAR PROPOSAL PROYEK AKHIR MAHASISWA DEPARTEMEN STATISTIKA BISNIS FAKULTAS VOKASI ITS SEMESTER GASAL 2023/2024')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (nama_mahasiswa, nrp, dosen_pembimbing, co_pempimbing, penguji, ruang, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        mahasiswa_name_lama = result["Nama Mahasiswa"]
        nrp_lama = result["NRP"]
        dosen_pembimbing_lama = result["Dosen Pembimbing"]
        co_pempimbing_lama = result["CO-Pembimbing"]
        penguji_lama = result["Penguji"]
        ruang_lama = result["Ruang"]
        waktu_lama = result["Waktu"]
        tanggal_lama = result["Tanggal"]

        with st.expander(f'a.n. {mahasiswa_name_lama}'):
            with st.form(f'data-{id}'):
                mahasiswa_name_baru = st.selectbox("mahasiswa_name", list_mahasiswa, list_mahasiswa.index(mahasiswa_name_lama))
                nrp_baru = st.text_input("nrp", nrp_lama)
                dosen_pembimbing_baru = st.selectbox("dosen_pembimbing", list_co_pembimbing, list_co_pembimbing.index(dosen_pembimbing_lama))
                co_pembimbing_baru = st.text_input("co_pembimbing", co_pembimbing_lama)
                penguji_baru = st.multiselect("penguji", ['Dra.Lucia Aridinanti,MS', 'Dr.Drs.Brodjol Sutijo Supri Ulama', 'Dr.Wahyu Wibowo,S.Si,M.Si', 'Dwi Endah Kusrini,S.Si,M.Si', 'Dra.Destri Susilaningrum,M.Si', 'Iis Dewi Ratih,S.Si.,M.Si', 'Zakiatul Wildani,S.Si.,M.Sc', 'Dra.Sri Mumpuni Retnaningsih,MT', 'Mukti Ratna Dewi,S.Si.,M.Sc', 'Muhammad Alfian Nuriman' ], eval(penguji_lama))
                ruang_baru = st.text_input("ruang", ruang_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE schedule \
                                          SET mahasiswa_name=:1,nrp=:2, dosen_pembimbing=:3, co-pembimbing=:4, \
                                          penguji=:5, ruang=:6, waktu=:7, tanggal=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':mahasiswa_name_baru, '2':nrp_baru, '3':dosen_pembimbing_baru, '4':co_pembimbing(co_pembimbing_baru), 
                                                    '5':'penguji(penguji_baru)', '6':ruang_baru, '7':waktu_baru, '8':tanggal_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()