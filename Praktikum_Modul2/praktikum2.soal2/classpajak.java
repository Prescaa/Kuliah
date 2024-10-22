package praktikum2.soal2;

class Kopi {
    String namaKopi;
    String ukuran;
    String namapembeli;
    double harga;

    public void info() {
        System.out.println("Nama Kopi: " + namaKopi);
        System.out.println("Ukuran: " + ukuran);
        System.out.println("Harga: Rp." + harga);
    }

    public void setPembeli(String namapembeli) {
        this.namapembeli = namapembeli;
    }

    public String getPembeli() {
        return namapembeli;
    }

    public double getPajak() {
        return 0.11 * harga;
    }
}
