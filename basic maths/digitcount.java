
import java.util.Scanner;


public class digitcount{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("enter a digit:");
        int N = sc.nextInt();

        while(N>0){
            int rem=N%10;
            N = N/10;
            System.out.println("digits"+rem);
        }
        sc.close();

    }
}
