package com.presca.utsmobile

data class Mahasiswa(
    val nama: String = "Rifky Putra Mahardika",
    val nim: String = "2310817210023",
    val jurusan: String = "Teknologi Informasi",
    val semester: Int = 4,
    val ipk: String = "3.70",
    val fotoRes: Int = R.drawable.fotomhs,
    val bio: String = """
        Halo perkenalkan, Nama saya Rifky Putra Mahardika dengan NIM 2310817210023 dengan Program Studi Teknologi Informasi. Saya lahir di Tabalong, 5 Oktober 2004. Hobi saya adalah bermain GeoGuessr, bermain media sosial, dan tidur.
        
        Saya merupakan mahasiswa semester 4 dengan IPK yang cukup memuaskan selama berkuliah. Saya memiliki minat dalam bidang Web Development serta tertarik pada karya tulis ilmiah (KTI) dan esai. Saat ini saya aktif dalam dua organisasi, yaitu Himpunan Mahasiswa Teknologi Informasi dan UKM PP FIM ULM. 
        
        Himpunan Mahasiswa Teknologi Informasi adalah organisasi kemahasiswaan di tingkat program studi yang memberikan berbagai pengalaman. Mulai dari kegiatan kepanitiaan seperti Ramadhan Bersama TI, Workshop Web Developer dan KTI, hingga Benchmarking dan kegiatan menarik lainnya.
        
        Sedikit kisah hidup saya, saya memiliki teman yang cukup banyak di kampung halaman saya, yaitu Tabalong. Selain itu, Banjarmasin sudah menjadi salah satu bagian tempat dalam kehidupan saya. Saya diajarkan kemandirian, keberanian, dan sifat introvert saya yang mulai berkurang dan mulai sering berosialisasi dengan banyak orang.
        
        Selain hobi bermain GeoGuessr dan bermain media sosial, saya suka sekali melakukan road trip di waktu luang saya, misalnya berkeliling Kota Banjarmasin ataupun ke kota tetangga seperti Kota Banjarbaru atau Kabupaten Kapuas.
    """.trimIndent(),
    val email: String = "rifkymahardika938@gmail.com",
    val noHp: String = "085332123015"
)
