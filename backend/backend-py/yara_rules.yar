rule spyware {
    meta :
        description = "Spyware"
        author = "Kshitij khatri"
        date = "09/04/2025"
    strings:
    // Suspious API calls 
        $api1 = "GetAsyncKeyState" ascii wide nocase 
        $api2 = "GetForegroundWindow" ascii wide nocase 
        $api3 = "GetClipboardData" ascii wide nocase 
        $api5 = "NtQueryInformationProcess" ascii wide nocase

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
    
    condition:
        2 of ($api*,$reg*, $pwd*, $net*)
}

rule Virus{
    meta:
        description = "Detects common malware/virus patterns in EXE, DLL, BAT files"
        author = "kshitij khatri"
        date = "2025/09/04"

    strings:
        // Suspicious APIs
        $api1 = "CreateRemoteThread" ascii wide
        $api2 = "WriteProcessMemory" ascii wide
        $api3 = "VirtualAllocEx" ascii wide

        $reg1 = "schtasks /create" ascii wide

        // BAT / Script Malware
        $bat1 = "del /f /q" ascii
        $bat2 = "taskkill /f" ascii
        $bat3 = "reg delete" ascii

    condition:
       2 of ($api*, $reg1, $bat*)


}

rule hack_tool {
    meta:
        description = "hack-tool"
        author = "Kshitij khatri"
     strings:
        // Tool-specific strings
        $nmap1 = "nmap.org" ascii
        $nmap2 = "Nmap version" ascii
        $nmap3 = "scan initiated" ascii
        $metasploit1 = "Metasploit Framework" ascii
        $metasploit2 = "exploit" ascii
        $metasploit3 = "payload" ascii
        $john1 = "John the Ripper" ascii
        $john2 = "crack" ascii
        $cain1 = "Cain" ascii
        $cain2 = "password recovery" ascii
        $hydra1 = "Hydra" ascii
        $hydra2 = "brute force" ascii
        $wireshark1 = "Wireshark" ascii
        $wireshark2 = "libpcap" ascii

        // Generic hacking-related functions
        $func1 = "socket" ascii
        $func2 = "connect" ascii
        $func3 = "hash" ascii
        $func4 = "sniff" ascii nocase
        $func5 = "brute" ascii nocase
        $func6 = "scan" ascii nocase

        // Common libraries or patterns
        $lib1 = "libpcap" ascii
        $lib2 = "openssl" ascii
        $lib3 = "libssh" ascii

    condition:
        (
            any of ($nmap*, $metasploit*, $john*, $cain*, $hydra*, $wireshark*) or
            (any of ($func*) and any of ($lib*)) or
            (3 of ($func*, $lib*))
        )
}


