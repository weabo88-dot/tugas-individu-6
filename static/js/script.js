$(function () {
    // ===== Audio (tombol ada di navbar semua halaman) =====
    const audio = document.getElementById("bg-audio");
    $("#btnAudio").on("click", function () {
        if (!audio) return;
        if (audio.paused) {
            audio.play();
            $(this).text("♫ pause");
        } else {
            audio.pause();
            $(this).text("♫ click to play");
        }
    });

    // ===== Cari mata kuliah (hanya ada di halaman Nilai) =====
    $("#inputCari").on("keyup", function () {
        const keyword = $(this).val().toLowerCase();
        let ditemukan = 0;
        $("#tabelNilaiBody tr").each(function () {
            const cocok = $(this).find("td:eq(2)").text().toLowerCase().includes(keyword);
            $(this).toggle(cocok);
            if (cocok) ditemukan++;
        });
        $("#pesanKosong").toggleClass("d-none", ditemukan > 0);
    });

    // ===== Tambah tugas (hanya ada di halaman Nilai) =====
    $("#formTugas").on("submit", function (e) {
        e.preventDefault();

        const $inputNama = $("#namaTugas");
        const $pesan = $("#pesanValidasi");
        const nilaiInput = $inputNama.val().trim();

        if (nilaiInput.length < 3) {
            $pesan.text("Nama tugas minimal harus 3 karakter!")
                  .removeClass("text-success").addClass("text-danger")
                  .stop(true, true).show();
            return;
        }

        $pesan.text("Berhasil menambahkan tugas: " + nilaiInput)
              .removeClass("text-danger").addClass("text-success")
              .stop(true, true).hide().fadeIn(300).delay(2000).fadeOut(300);

        const $item = $(`
            <li class="list-group-item bg-dark text-light border-secondary d-flex justify-content-between align-items-center">
                <span></span>
                <button class="btn btn-outline-danger btn-sm btn-hapus">Hapus</button>
            </li>`);
        $item.find("span").text(nilaiInput);   // .text() agar aman dari injeksi HTML
        $("#listTugas").append($item);
        $inputNama.val("");
    });

    $("#listTugas").on("click", ".btn-hapus", function () {
        $(this).closest("li").fadeOut(200, function () { $(this).remove(); });
    });
});