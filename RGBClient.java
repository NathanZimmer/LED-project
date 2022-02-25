import java.net.*;
import java.io.*;

public class RGBClient {
    private static Socket clientSocket;
    private static DataOutputStream out;
    private static DataInputStream in;

    // starts connection and creates output stream
    public void StartConnection(String host, int port) {
        try {
            clientSocket = new Socket(host, port);
            out = new DataOutputStream(clientSocket.getOutputStream());
            in = new DataInputStream(clientSocket.getInputStream());
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

    // gets int message from server and returns -1 if something goes wrong
    public byte GetMessage() {
        try {
            return in.readByte();
        }
        catch(Exception e) {
            System.out.println(e);
            return (byte)-1;
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