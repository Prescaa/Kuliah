import java.util.Scanner;

public class PRAK102_2310817210023_RIFKYPUTRAMAHARDIKA {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Input: ");
        int Angka = input.nextInt();
        int Baris = 0;
        
        System.out.print("Output: ");
        while (Baris < 11) { 
            if (Angka % 5 == 0) {
                System.out.print(Angka / 5 - 1);
            } else {
                System.out.print(Angka);
            }
            if (Baris < 10) {
                System.out.print(", ");
            }
            
            Baris++;
            Angka++;

        }
    }
}
