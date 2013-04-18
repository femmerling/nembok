# Deskripsi

**nembok** adalah portal komunikasi code sprint untuk python coders
Indonesia.

Motivasi kami adalah untuk memiliki sarana berbagi bersama yang secara
cepat dan juga sebagai ajang saling kenal antara coder Python nusantara.

# Instalasi

Untuk melakukan instalasi cukup clone repo dengan menjalankan:

    git clone git://github.com/femmerling/nembok.git

Jalankan setup dengan menjalankan:

    python setup.py

Setelah selesai, sesuaikan config database pada file `config.py`.

Jalankan test server dengan menggunakan:

    ./box.py -t

Jalankan production server dengan menggunakan:

    ./box.py -g

# Kolaborasi

1. Fork repo `nembok`.
2. Set remote URL, contoh: `git remote add upstream git://github.com/femmerling/nembok.git`.
3. Buat topic branch, contoh: `git checkout -b feature-A`.
4. Develop feature yang Anda inginkan, lalu push branch `feature-A`.
5. Pull request ke repo ini.
