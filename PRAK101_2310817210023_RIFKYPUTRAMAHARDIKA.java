import java.util.Scanner;

public class PRAK101_2310817210023_RIFKYPUTRAMAHARDIKA {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Masukkan Nama Lengkap: ");
        String NamaLengkap = input.nextLine();
        
        System.out.print("Masukkan Tempat Lahir: ");
        String TempatLahir = input.nextLine();
        
        System.out.print("Masukkan Tanggal Lahir: ");
        String Tanggal = input.nextLine();
        
        System.out.print("Masukkan Bulan Lahir: ");
        String Bulan = input.nextLine();
        
        System.out.print("Masukkan Tahun Lahir: ");
        String Tahun = input.nextLine();
        
        System.out.print("Masukkan Tinggi Badan: ");
        String Tinggi = input.nextLine();
        
        System.out.print("Masukkan Berat Badan: ");
        String BeratBadan = input.nextLine();
        
        switch (Bulan) {
        case "1": Bulan = "Januari"; break;
        case "2": Bulan = "Februari"; break;
        case "3": Bulan = "Maret"; break;
        case "4": Bulan = "April"; break;
        case "5": Bulan = "Mei"; break;
        case "6": Bulan = "Juni"; break;
        case "7": Bulan = "Juli"; break;
        case "8": Bulan = "Agustus"; break;
        case "9": Bulan = "September"; break;
        case "10": Bulan = "Oktober"; break;
        case "11": Bulan = "November"; break;
        case "12": Bulan = "Desember"; break;
        default: Bulan = "Bulan tidak valid"; break;
    }
        
        System.out.println("Nama Lengkap " + NamaLengkap + ", Lahir di " + TempatLahir + " pada Tanggal " + Tanggal + " " + Bulan + " " + Tahun + " Tinggi Badan " + Tinggi +" cm dan Berat Badan " + BeratBadan + " kilogram");
        }
    }
