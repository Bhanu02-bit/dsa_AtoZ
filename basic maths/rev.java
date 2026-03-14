
import java.util.Scanner;


public class rev{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("enter a digit:");
        int N = sc.nextInt();
        int rev=0;

        while(N>0){
          
            int rem=N%10;
            N = N/10;
            rev=rev*10+rem;
            
        }
        System.out.println("digits"+rev);
        sc.close();

    }
}
