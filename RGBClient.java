import java.net.*;
import java.io.*;

public class RGBClient {
    private static Socket clientSocket;
    private static DataOutputStream out;

    // starts connection and creates output stream
    public void StartConnection(String host, int port) {
        try {
            clientSocket = new Socket(host, port);
            out = new DataOutputStream(clientSocket.getOutputStream());
        }
        catch(ConnectException e) {
            System.out.println("Server not found or connection was refused. Make sure IP and port are correct.");
            System.exit(0);
        }
        catch(Exception e) {
            System.out.print(e);
        }
    }

    // method for sending message to socket
    public void SendMessage(int[] data) {
        try {
            out.writeByte(0); // for some reason the first byte of data is received seperatly from the rest. I can't fix it so I'm sending a byte to be ignored.
            for (int i = 0; i < data.length; i++) {
                out.writeByte(data[i]);
            }
            out.flush();
        }
        catch(Exception e) {
            System.out.println(e);
        }
    }

    // closes connection when called
    public void StopConnection() {
        try {
            out.close();
            clientSocket.close();
        }
        catch(Exception e) {
            System.out.println(e);
        }
    }
}