// hello 

rule spyware_rules {
    meta :
        description = "Spyware"
        author = "Kshitij khatri"
        date = "09/04/2025"
    strings:
    // Suspious API calls 
        $api1 = "GetAsyncKeyState" ascii wide nocase 
        $api2 = "GetForegroundWindow" ascii wide nocase 
        $api3 = "GetClipboardData" ascii wide nocase 
        $api4 = "CreateRemoteThread" ascii wide nocase 
        $api4 = "NtQueryInformationProcess" ascii wide nocase

    // Registry persistance 
        $reg1 = "Software\\Microsoft\\Windows\\CurrentVersion\\Run" ascii wide nocase 
        $reg2 = "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce" ascii wide nocase

    // Password / browser data Theft 
        $pwd1 = "Google\\Chrome\\User Data" ascii wide nocase 
        $pwd2 = "Mozilla\\Firefox\\Profiles" ascii wide nocase 
        $pwd3 = "Internet Explorer\\IntelliForms" ascii wide nocase 

    // Network exfiltration 
        $net1 = "User-Agent:" ascii nocase 
        $net2 = "Content-type: appilication/x-www-form-urlencoded" ascii nocase 
        $net3 = "POST / HTTP/1.1" ascii nocase 

    // Keylogger hints 
        $kil1 = "keylog" ascii nocase 
        $kil2 = "keystroke" ascii nocase 
        $kil3 = "keyboardState" ascii nocase 

    // Obfuscation / packers 
        $pack1 = "URX!" ascii 
        $pack2 = "ASPack" ascii
        $pack3 = "Themida" ascii 

    // File path target 
        $fp1 = "\\AppData\\Roaming\\" ascii wide nocase
        $fp2 = "\\Temp\\" ascii wide nocase
    
    condition:
        3 of ($api*, $reg*, $pwd*, $net*, $kil*, $pack*, $fp*)
}