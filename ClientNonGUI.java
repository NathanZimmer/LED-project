import static java.lang.System.out;
import java.util.*;

public class ClientNonGUI {
    private static Scanner scanner = new Scanner(System.in);
    public static void main(String[] args) {
        // config- change these values depending on the IP of your raspberry pi and the port of the server
        String host = "192.168.1.69"; 
        int port    = 65432;       

        // connecting to server
        RGBClient client = new RGBClient();
        client.StartConnection(host, port);
        
        // getting user input
        while (true) {
            out.println("0: solid color");
            out.println("1: gradient");
            out.println("2: color fade");
            out.println("3: color bands");
            out.println("4: change brightness");
            out.println("5: off");
            out.println("6: get status");
            out.println("7: close program");
            int choice = getInput();

            LinkedList<Integer> inputList = new LinkedList<>();
            inputList.add(choice);
            
            // solid color
            if (choice == 0) {
                out.println("Enter r, g, and b values separated by spaces:");

                for (int i = 0; i < 3; i++) {
                    inputList.add(getInput());
                }

                out.println("Enable color chase? (1 for true, 0 for false):");
                int chase = getInput();
                inputList.add(chase);
                
                int speed = 0;
                if (chase == 1) {
                    out.println("Chase speed (smaller is faster):");
                    speed = getInput();
                }
                inputList.add(speed);   
            }
            // gradient
            else if (choice == 1) {
                out.println("Enter two sets of rgb values separated by spaces:");

                for (int i = 0; i < 6; i++) {
                    inputList.add(getInput());
                }

                out.println("Enter offset for first color:");
                inputList.add(getInput());

                out.println("Enter offset for second color:");
                inputList.add(getInput());

                out.println("Enable color chase? (1 for true, 0 for false):");
                int chase = getInput();
                inputList.add(chase);
                
                int speed = 0;
                if (chase == 1) {
                    out.println("Chase speed (smaller is faster):");
                    speed = getInput();
                }
                inputList.add(speed);  
            }
            // color fade
            else if (choice == 2) {
                out.println("Enter at least 2 rgb values separated by spaces:");
                inputList.addAll(getMultiInput());

                out.println("Enter fade speed:");
                inputList.add(getInput());
            }
            // color bands
            else if (choice == 3) {
                out.println("Enter at least 2 rgb values separated by spaces:");
                inputList.addAll(getMultiInput());

                out.println("Enter number of iterations each color should have:");
                inputList.add(getInput());

                out.println("Enter size of gradient between each color (1 means no gradient):");
                inputList.add(getInput());

                out.println("Movement speed:");
                inputList.add(getInput());

                out.println("enable movement? (1 for yes, 0 for no):");
                inputList.add(getInput());
            }
            // changing brightness
            else if (choice == 4) {
                out.println("Enter brightness:");
                inputList.add(getInput());
            }
            // closing program
            else if (choice == 7) {
                break;
            }
            
            // sending array to server
            int[] inputArray = inputList.stream().mapToInt(Integer::intValue).toArray();
            client.SendMessage(inputArray);

            if (choice == 6) {
                out.println(client.GetMessage());
            }
        }
        scanner.close();
    }

    // repeatedly prompts the user for a value until a valid value (a non-negative int) is entered. returns that value
    private static int getInput() {
        while (true) {
            try {
                int input = scanner.nextInt();
                if (input < 0)
                    throw new InputMismatchException();
                return input;
            }
            catch(InputMismatchException e) {
                out.println("Invalid input. Enter a non-negative int:");
                scanner.next();
            }
        }
    }

    // reads a line and returns a linkedList of int. user should enter int values separted by spaces
    private static LinkedList<Integer> getMultiInput() {
        LinkedList<Integer> inputList = new LinkedList<>();
        scanner.nextLine();

        String input = scanner.nextLine();
        String input_array[] = input.split(" ");

        for (int i = 0; i < input_array.length; i++) {
            String value = input_array[i].replaceAll(" ", "");
            inputList.add(Integer.parseInt(value));
        }
        return inputList;
    }
}