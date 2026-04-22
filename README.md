# Medical-Android-App-Data-Leakage
Static analysis tool for detecting potential privacy leaks in Android fitness apps by analyzing APK files, permissions, and data flow patterns.

What the Project Does 
This tool takes an Android APK file and analyzes it to find possible privacy risks. It looks for: 
 
    •	Permissions requested by the app 
    
    •	Sensitive data sources (like location or device ID) 
    
    •	Data sinks (where data may be sent, such as network connections) 
    
    •	Third-party libraries (like Firebase, AdMob, Facebook SDK) 
    
    •	Possible data leaks (when a source and sink appear together) 

The tool then calculates a risk score and generates results.

How It Works 
The system follows a simple pipeline: 
 
    •	Decompile the APK using APKTool 
  
    •	Extract all relevant files (Java, Kotlin, Smali, XML) 
    
    •	Read permissions from the AndroidManifest file 
    
    •	Scan files for sensitive sources and sinks 
    
    •	Detect possible leaks based on source and sink patterns 
    
    •	Identify third-party libraries and URLs 
    
    •	Calculate a risk score 
    
    •	Generate results in JSON and HTML format

Project Structure 

      •	main.py - Runs the full analysis pipeline 
      
      •	config.py - Stores patterns for sources, sinks, and SDKs 
      
      •	fileextraction.py - Extracts relevant files 
      
      •	permissions.py - Reads app permissions 
      
      •	scanner.py - Scans files for sources, sinks, URLs, SDKs 
      
      •	leaks.py - Detects possible leaks 
      
      •	riskcalc.py - Calculates risk score 
      
      •	analysis.py - Organizes and saves results 
      
      •	report_html.py - Generates HTML report

How to Run 
      
      1.	Install APKTool 
     
      2.	Place your APK file in the project directory 

      3. Decompile using APKTool
       - apktool d app.apk -o output/
      
      3.	Run: python main.py
       - main.py [-h] [--app APP] [--output OUTPUT] [--html HTML] directory
       - -h -> Path to decompiled APK directory
       - --app -> App name/identifier
       - --output -> Output JSON file path
       - --html -> Optional: output HTML report file path
       
The tool will: 
      
      •	Analyze the files 

      • Determine potential leaks, permissions, third-party libraries, etc.

      • Calculate risk score
      
      •	Generate results

Output 

The tool generates: 

      •	JSON file with analysis results 
      
      •	HTML report for easy viewing 

The HTML report includes: 

      •	Risk score 
      
      •	Number of leaks 
      
      •	Permissions 
      
      •	Third-party libraries 
      
      •	Detected sources and sinks

Example Use Case 

This tool was used to analyze fitness apps such as: 

      •	Cronometer 
      
      •	FitnessOnline 
      
      •	MyFitnessPal 
      
      •	Fitbod 
      
      •	Google Fit 
      
      •	Mi Fitness 

The results showed that some apps have higher privacy risks due to data leaks and third-party tracking.

Limitations 

      •	Uses static analysis (does not run the app) 
      
      •	May produce false positives 
      
      •	Cannot confirm actual data transmission 
      
      •	Some apps may not fully decompile

Future Improvements 

      •	Add data flow tracking 
      
      •	Improve detection of obfuscated code 
      
      •	Add dynamic analysis 
      
      •	Support more app categories

Authors 

      •	Ricardo Garcia 
      
      •	Natan Farhy 
      
      •	Sebastian Medina


      
