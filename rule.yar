rule spyware{
    meta:
        description = "this is spyware"

    strings:
        $a = "hello"
    condition:
        any of them
}

rule virus{
    meta : 
        description = "this is virus"
    strings:
        $b = "virus"
    condition:
        any of them
}