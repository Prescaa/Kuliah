package soal3;

import java.util.Scanner;
import java.util.ArrayList;

public class main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Mahasiswa> listMahasiswa = new ArrayList<>();
        int pilihan = 0;

        while(true) {
            System.out.println("\nMenu:");
            System.out.println("1. Tambah Mahasiswa");
            System.out.println("2. Hapus Mahasiswa berdasarkan NIM");
            System.out.println("3. Cari Mahasiswa berdasarkan NIM");
            System.out.println("4. Tampilkan Daftar Mahasiswa");
            System.out.println("0. Keluar");
            System.out.print("Pilihan: ");
            pilihan = input.nextInt();
            input.nextLine();

            int i;
            switch(pilihan) {
                case 1:
                    System.out.print("Masukkan Nama Mahasiswa: ");
                    String nama = input.nextLine();
                    System.out.print("Masukkan NIM Mahasiswa (harus unik): ");
                    String nim = input.nextLine();
                    Mahasiswa mahasiswaBaru = new Mahasiswa(nama, nim);
                    listMahasiswa.add(mahasiswaBaru);
                    System.out.println("Mahasiswa " + nama + " ditambahkan");
                    break;

                case 2:
                    System.out.print("Masukkan NIM Mahasiswa yang akan dihapus: ");
                    String nimHapus = input.nextLine();
                    
                    for (i = 0; i < listMahasiswa.size(); i++) {
                        if (nimHapus.equals(listMahasiswa.get(i).getNim())) {
                            listMahasiswa.remove(i);
                            System.out.println("Mahasiswa dengan NIM " + nimHapus + " berhasil dihapus.");
                            break;
                        } else if (i == listMahasiswa.size() - 1) {
                            System.out.println("Mahasiswa dengan NIM " + nimHapus + " tidak ditemukan.");
                        }
                    }
                    break;


                case 3:
                    System.out.print("Masukkan NIM dari Mahasiswa yang ingin dicari: ");
                    String nimCari = input.nextLine();
                    for (i = 0; i < listMahasiswa.size(); i++) {
                        if (nimCari.equals(listMahasiswa.get(i).getNim())) {
                            System.out.println("NIM: " + listMahasiswa.get(i).getNim() + ", Nama: " + listMahasiswa.get(i).getNama());
                            break;
                        }
                    }
                    
                    if (i == listMahasiswa.size()) {
                        System.out.println("Nim tidak ditemukan.");
                    }
                    break;

                case 4:
                    System.out.println("Daftar Mahasiswa:");
                    for(i = 0; i < listMahasiswa.size(); i++) {
                        System.out.println("NIM: " + listMahasiswa.get(i).getNim() + ", Nama: " + listMahasiswa.get(i).getNama());
                    }
                    break;

                case 0:
                    System.out.println("Terima kasih!");
                    input.close();
                    System.exit(0);

                default:
                    System.out.println("Pilihan harus sesuai dengan menu!");
            }
        }
    }
}
