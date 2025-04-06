r"""
  ___                   __                 __             __          __ __       
 |   .-----.--.--.-----|  |--.-----.______|__.--.--.-----|  |--.-----|__|  .-----.
 |.  |     |  |  |  _  |    <|  -__|______|  |  |  |     |    <|  _  |  |  |  -__|
 |.  |__|__|\___/|_____|__|__|_____|      |  |_____|__|__|__|__|   __|__|__|_____|
 |:  |                                   |___|                 |__|               
 |::.|                                                                            
 `---'                                                                            
     
Invoke-Junkpile: Built to execute, not understood...

This tool takes clean PowerShell scripts and transforms them into an
entropic pile of randomly stacked variables disquised as PowerShell 
commands, obfuscated strings, and execution confusion. Useful for 
evading signature-based detection, annoying static analysis tools, 
and confusing SOC analysis...


Author: Tim Peck (@bobby-tablez)
GitHub: https://github.com/bobby-tablez
Version: 1.0
"""
import argparse
import random
import base64
import re


rand = lambda: str(random.randint(0, 9))

# Commonly used cmdlets
cmdlets = [
    'Get-Service', 'Get-Process', 'Clear-RecycleBin', 'Test-NetConnection',
    'Get-Date', 'Restart-Service', 'Stop-Process', 'Get-WmiObject',
    'Get-ChildItem', 'Get-EventLog', 'New-Item', 'Get-Help',
    'Remove-Item', 'Invoke-WebRequest', 'Start-Sleep', 'Get-Content',
    'Write-Output', 'Write-Host', 'Write-Warning', 'Write-Error', 'Read-Host',
    'Get-Hotfix', 'Get-Location', 'ConvertTo-Json', 'Compress-Archive',
    'Expand-Archive', 'Get-NetAdapter', 'Import-Module', 'ForEach-Object',
    'Where-Object'
]

# parameters
parameters = [
    '-ArgumentList', '-Force', '-Verbose', '-Debug', '-InputFormat',
    '-OutputFormat', '-ErrorAction SilentlyContinue', '-ErrorAction Stop',
    '-Confirm $False', '-InformationAction Continue'
]

# randomized parameter values
parameter_values = [
    ('-Name', [
        'WinRM', 'CcmExec', 'explorer', 'svchost', 'lsass', 'conhost',
        'powershell', 'msedge', 'Teams', 'OneDrive', 'wscript', 'cmd'
    ]),
    ('-ComputerName', [
        'localhost',
        f"$server_ip_0{rand()}", f"$server_ip_0{rand()}", f"$server_ip_0{rand()}",
        f"$workstation0{rand()}", f"$workstation0{rand()}", f"$workstation0{rand()}",
        f"$dc_0{rand()}", f"$dc_0{rand()}", f"$dc_0{rand()}",
        '$router_ip', '$pingtest', '127.0.0.1'
    ]),
    ('-InformationLevel', [
        'Quiet', 'Detailed', 'Debug', 'Minimal', 'Verbose', 'Silent'
    ]),
    ('-Path', [
        '\\\\Windows\\System32', '.\\Temp', '%USERPROFILE%', '%TEMP%', '%APPDATA%',
        '\\\\Program Files', '.\\Logs', '\\\\Backups', '\\\\ShareSpace\\Scripts'
    ]),
    ('-Class', [
        'Win32_OperatingSystem', 'Win32_ComputerSystem', 'Win32_Process',
        'Win32_Service', 'Win32_LogicalDisk', 'CIM_LogicalElement'
    ]),
    ('-LogName', [
        'System', 'Application', 'Security', 'Setup', 'Windows PowerShell',
        'Microsoft-Windows-Sysmon/Operational'
    ]),
    ('-DestinationPath', [
        '.\\Backups', '.\\Data', '%USERPROFILE%', '%TEMP%', '%APPDATA%',
        '.\\Archive', '.\\Quarantine', '.\\Extracted'
    ]),
    ('-Uri', [
        'login.microsoftonline.com/common/oauth2/v2.0/token',
        'graph.microsoft.com/v1.0/me',
        'portal.azure.com/#home',
        'outlook.office365.com/mail/inbox',
        'login.windows.net/common/oauth2/authorize',
        'management.azure.com/subscriptions',
        'login.live.com/oauth20_authorize.srf',
        'aka.ms/powershell',
        'office365.com/?auth=1',
        'security.microsoft.com/incidents',
        'compliance.microsoft.com/auditlogsearch',
        'admin.microsoft.com/AdminPortal/Home#/homepage',
        'autologon.microsoftazuread-sso.com/winauth/sso',
        'aadcdn.msftauth.net/ests/2.1/content/cdnbundles',
        'aadcdn.msauth.net/shared/1.0/content',
        'cdn.office.net/files/configuration.xml',
        'outlook.office.com/owa/',
        'accounts.google.com/o/oauth2/v2/auth',
        'www.googleapis.com/drive/v3/files',
        'admin.google.com/ac/home',
        'mail.google.com/mail/u/0/#inbox',
        'drive.google.com/drive/my-drive',
        'docs.google.com/document/u/0/',
        'calendar.google.com/calendar/u/0/r',
        'hangouts.google.com/webchat/start',
        'meet.google.com/lookup',
        'www.google.com/a/domain.com/ServiceLogin',
        'workspace.google.com/solutions/',
        'oauth2.googleapis.com/token',
        'apis.google.com/js/platform.js',
        'lh3.googleusercontent.com/a-/AOh14Gh',
        'ssl.gstatic.com/ui/v1/icons/mail/images'
    ]),
    ('-Seconds', [str(random.randint(1, 30)) for _ in range(8)])
]

# Remove any contained comments before processing, this keeps the overall generated codebase down as much as possible
def strip_comments(ps_code):
    # standard comment blcoks
    no_block = re.sub(r'<#.*?#>', '', ps_code, flags=re.DOTALL)
    
    # match on single line
    no_single = re.sub(r'(?m)^[ \t]*#.*?$|(?<!")\s+#.*$', '', no_block)

    return no_single


# Stuff random code garbage throughout
def generate_dead_code():
    return random.choice([
        "\n\n", # 
        "\n\n", # Empty filler lines to skew entropy checks
        "\n\n", #
        "\n\n", #
        f"\n$test0{rand()} = {rand()}",
        f"\n$backupcount = {rand()}",
        f"\n$Win32_count = {rand()}",
        f"\n$set_scaler_{rand()}{rand()} = {rand()}{rand()}{rand()}",
        f"\nif ($false) {{ $x = {rand()} }}",
        f"\nwhile ($binpath) {{ Start-Sleep -Seconds {rand()} }}",
        f"\ntry {{ $y = {rand()} }} catch {{ $error }}",
        f"\nfor ($i = 0; $i -lt {rand()}; $i++) {{ $nextvar = $i }}",
        f"\nwhile ($null) {{ $run = {rand()}; Start-Sleep -Seconds {rand()} }}",
        f"\nif ($completion -eq $null) {{ $count = {rand()} }}",
        f"\ntry {{ Remove-Item -Path \"C:\\temp\\logfile_{rand()}.txt\" -ErrorAction SilentlyContinue }} catch {{ Start-Sleep -Seconds {rand()} }}",
        f"\nfor ($j = 0; $j -lt {rand()}; $j++) {{ $final += $j }}",
        f"\nwhile ($counter -lt {rand()}) {{ $counter++ }}",
        f"\nif ($errorLevel -gt {rand()}) {{ Write-Output '$result' }}",
        f"\ntry {{ $void = Get-Random -Minimum {rand()} -Maximum {int(rand()) + 5} }} catch {{ $void = $null }}",
        f"\n$randIndex = Get-Random -Minimum {rand()} -Maximum {int(rand()) + 10}"
    ])

used_vars = set()

# Final generator for random variables
def generate_var():
    while True:
        cmd = random.choice(cmdlets)
        param = random.choice(parameters)
        name, values = random.choice(parameter_values)
        val = random.choice(values)

        # Throw in extra randomness disquised as variables to prevent variable collisions on large scripts
        suffix = ''.join(random.choices('abcdefghiklmnoprst', k=random.randint(3, 6)))
        var_name = f"${{{cmd} {param} {name} {val} && (${suffix})}}"
        
        if var_name not in used_vars:
            used_vars.add(var_name)
            return var_name


# break B64 string into chunks and generate randomly stacked lines of variables
def chunk_and_obfuscate(encoded_script, debug=False):
    chunks = []

    i = 0
    while i < len(encoded_script):
        chunk_len = random.randint(4, 15)
        chunks.append(encoded_script[i:i + chunk_len])
        i += chunk_len

    if debug:
        print(f"[DEBUG] Total chunks: {len(chunks)}")

    var_map = {}
    assignments = []
    for chunk in chunks:
        var = generate_var()
        var_map[chunk] = var
        assignments.append(f"{var} = \"{chunk}\"")

    if debug:
        print(f"[DEBUG] Sample chunk+var: {assignments[0]}")

    grouped_lines = []
    i = 0

    while i < len(assignments):
        group_size = random.randint(1, 3) # Range or amount of stacking to perfrom on newly created variables
        grouped_lines.append(";".join(assignments[i:i+group_size]) + ";")
        for _ in range(3): grouped_lines.append(generate_dead_code()) # modify range number to apply more/less dead code between generated strings
        i += group_size

    ordered_vars = [var_map[chunk] for chunk in chunks]

    return grouped_lines, ordered_vars, chunks

# Small function to mess with whitespace, thanks ChatGPT :')
def split_str(s):
    parts = []

    i = 0
    while i < len(s):
        remaining = len(s) - i
        chunk = random.randint(1, min(4, remaining))
        parts.append("'" + s[i:i+chunk] + "'")
        i += chunk

    # Random space per join
    spaced = parts[0]
    for part in parts[1:]:
        space_before = ' ' * random.randint(1, 10)
        space_after = ' ' * random.randint(1, 10)
        spaced += f"{space_before}+{space_after}{part}"

    return spaced


# Create last line in script which executes the compiles base64 string (To do: more randomized obfuscation for iex)
def generate_execution_line_array_style(array_var, debug=False):
    def split_str(s):
        parts = []
        i = 0
        while i < len(s):
            chunk = random.randint(1, min(4, len(s) - i))
            space = ' ' * random.randint(1, 12)
            parts.append(f"'{s[i:i+chunk]}'")
            i += chunk
        return f" +{space}".join(parts)

    final_var = generate_var()
    trailing_var = generate_var()
    utf8 = f"[Text.Encoding]::({split_str('UTF8')})"
    getstring = f".({split_str('GetString')})"
    frombase64 = f"::({split_str('FromBase64String')})"
    convert = f"[Convert]{frombase64}"

    join_chunks = f"{final_var} = {array_var} -join \"\""
    decode_line = f"{utf8}{getstring}({convert}({final_var})) | IEX"
    trailing_line = f"{trailing_var} = {random.randint(100,999)}"

    combo_line = f"{join_chunks}; {decode_line}; {trailing_line}"

    # Add 7–10 junk lines after IEX to bury it
    junk_lines = []

    for _ in range(random.randint(7, 10)):
        junk_var = generate_var()
        junk_value = random.randint(0, 999)
        junk_lines.append(f"{junk_var} = {junk_value}")
        junk_lines.append(generate_dead_code())

    if debug:
        print(f"[DEBUG] Final var: {final_var}")
        print(f"[DEBUG] IEX var: {trailing_var}")
        print(f"[DEBUG] Obfuscated exec line:\n{combo_line}")


    return "\n".join([combo_line] + junk_lines)


# Generator for producing the final array of permutated variables containing base64
def wrap_final_string(var_names, debug=False):
    chunk_array_var = generate_var()  # random fake cmdlet-style var like ${Get-Help -Verbose -Path .\Temp && ($xyrt)}
    lines = [f"{chunk_array_var} = @()"]

    i = 0
    while i < len(var_names):
        group_size = random.randint(3, 7) # modify stacked strings separated by ;
        group = var_names[i:i + group_size]
        lines.append(f"{chunk_array_var} += @({', '.join(group)})")
        for _ in range(3): lines.append(generate_dead_code()) # modify range number to apply more/less dead code between generated strings
        i += group_size

    # Execution line using array join
    lines.append(generate_execution_line_array_style(chunk_array_var, debug))

    return "\n".join(lines)


# main obfuscation function for base64 handling
def obfuscate_script(input_code, debug=False):
    stripped_code = strip_comments(input_code)
    encoded = base64.b64encode(stripped_code.encode()).decode()

    if debug:
        print(f"[DEBUG] Encoded base64 length: {len(encoded)}")
        print(f"[DEBUG] First 60 base64 chars: {encoded[:60]}...")

    try:
        base64.b64decode(encoded)

    except Exception as e:
        raise ValueError(f"[!] Error: Failed to base64 encode script: {e}")

    lines, vars_used, chunks = chunk_and_obfuscate(encoded, debug=debug)
    final_line = wrap_final_string(vars_used, debug=debug)

    # Validation: reconstruct $final from original chunks
    final_rebuild = ''.join(chunks)

    try:
        decoded = base64.b64decode(final_rebuild.encode()).decode(errors='ignore')
        if debug:
            print("[DEBUG] Final chunk-reconstruct base64 is valid.")
            print(f"[DEBUG] Decoded preview:\n{decoded.strip()[:120]}")

    except Exception as e:
        raise ValueError(f"[!] Error: Final $final is invalid base64. Check chunk generation.\n{e}")

    return "\n".join(lines + [final_line])



def main():
    parser = argparse.ArgumentParser(
        description=r"""\
 ___                   __                 __             __          __ __       
|   .-----.--.--.-----|  |--.-----.______|__.--.--.-----|  |--.-----|__|  .-----.
|.  |     |  |  |  _  |    <|  -__|______|  |  |  |     |    <|  _  |  |  |  -__|
|.  |__|__|\___/|_____|__|__|_____|      |  |_____|__|__|__|__|   __|__|__|_____|
|:  |                                   |___|                 |__|               
|::.|                                                                            
`---'                                                                          
    
Invoke-Junkpile: Built to execute, not understood...

Author: Tim Peck (@bobby-tablez)
GitHub: https://github.com/bobby-tablez
Version: 1.0

""",
    formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-f", "--file", help="Path to PowerShell script")
    parser.add_argument("-c", "--command", help="Inline PowerShell command string")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    if not (args.file or args.command):
        parser.print_help()
        return

    content = open(args.file, 'r', encoding='utf-8').read() if args.file else args.command

    try:
        obfuscated = obfuscate_script(content, debug=args.debug)

    except Exception as e:
        print(f"[!] Error during Junkpile creation:\n{e}")
        return

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(obfuscated)
        print(f"[+] Saved to {args.output}")

    else:
        print(obfuscated)

if __name__ ==  "__main__":
    main()