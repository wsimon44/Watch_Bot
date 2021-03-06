import java.util.ArrayList;
import java.util.List;
import java.util.TimerTask;
import java.util.Timer;

import javax.swing.JSpinner.ListEditor;

import rec.robotino.com.AnalogInput;
import rec.robotino.com.DigitalInput;
import rec.robotino.com.Bumper;
import rec.robotino.com.Com;
import rec.robotino.com.DistanceSensor;
import rec.robotino.com.Motor;
import rec.robotino.com.OmniDrive;

/**
 * The class Robot demonstrates the usage of the most common robot component classes.
 * Furthermore it shows how to handle events and receive incoming camera images.
 */
public class Robot
{
	//Pour les capteurs lumineux
	public native boolean valeurCptLumW(int numPin, String hostname);
	
	static {
		//System.loadLibrary("rec_robotino_com_c");
		System.loadLibrary("CptLumW");
	}
	
	protected final Com _com;
	protected final Bumper _bumper;
	
	public Robot()
	{
		_com = new Com();
		_bumper = new Bumper();

	}
	
	public boolean isConnected()
	{
		return _com.isConnected();
	}

	public void connect(String hostname)
	{
		System.out.println("Connecting...");
		_com.setAddress( hostname );
	}

	public void disconnect()
	{
		_com.disconnect();;
	}
	  
    public void readValue(String hostname)
    {

    	boolean valeurCptLumineux5;
		boolean valeurCptLumineux6;
		
		CptLumW classeValeurCptLumineux = new CptLumW();
		
		valeurCptLumineux5 = classeValeurCptLumineux.valeurCptLumW(5, hostname);
		System.out.println("JAVA 5 :" + valeurCptLumineux5);
		valeurCptLumineux6 = classeValeurCptLumineux.valeurCptLumW(6, hostname); //Celui-ci est defectueux sur Robotino .37
		System.out.println("JAVA 6 :" + valeurCptLumineux6);
	
		if(valeurCptLumineux5 && valeurCptLumineux6){
			System.out.println("Detection vide 2 capteurs");
		}
		else if(valeurCptLumineux5 || valeurCptLumineux6){
			System.out.println("Detection vide 1 capteur");
		}
		else{
			System.out.println("Sol");
		}
		
    }

	public static void main(String[] args) throws Exception
	{
		String hostname = System.getProperty("localhost", "193.48.125.37");
		//String hostname = System.getProperty("localhost", "127.0.0.1");
		Robot robotino = new Robot();		
		try
		{
			//robotino.connect(hostname, true);
			robotino.connect(hostname);
			robotino.readValue(hostname);
			robotino.disconnect();
		}
		catch (Exception e)
		{
			System.out.println(e.toString());
		}
	}
}