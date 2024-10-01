import java.util.Scanner;

public class PRAK103_2310817210023_RIFKYPUTRAMAHARDIKA {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
        
        System.out.print("Input: ");
        int N = input.nextInt();
        int Angka = input.nextInt();
        int Baris = 0;
        
        System.out.print("Output: ");
        do {
            if (Angka%2!=0) {
            	System.out.print(Angka);
            	Baris++;
            	if (Baris < N) {
            		System.out.print(", ");
            	}
            }
            Angka++;
        } while (Baris < N);
	}
}
