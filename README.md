# Invoke-Junkpile

> Built to execute, not to be understood...

![Invoke-Junkpile Banner](assets/banner.png)

## Overview

  [![PyPI Version](https://img.shields.io/pypi/v/invoke-junkpile)](https://pypi.org/project/invoke-junkpile/)
  [![PyPI Downloads](https://static.pepy.tech/badge/invoke-junkpile)](https://pepy.tech/projects/invoke-junkpile)

**Invoke-Junkpile** is a Python-based tool that takes clean PowerShell scripts and transforms them into an entropic mess of stacked polymorphic variables, junk code, and obfuscated logic through randomization. The generated code is designed to be obfuscated while not appearing obfuscated. Designed for stealth, this tool aims to evade static detection signatures, confuse reverse engineers, and wreak havoc on basic string-matching defenses and entropy checks. In the end, it outputs fully functional, heavily obfuscated PowerShell code.

This was tested on a wide range of PowerShell scripts which worked in 99% of cases (see limitations below). This includes very large and complex scripts and scripts containing assemblies. 

---

## Features

- **Base64 encoding:** done prior to obfuscation to preserve functionality.
- **Obfuscated chunking:** Script is split into chunks assigned to randomly named variables.
- **Chunk stacking:** Variable groups are randomly joined (2–7 chunks per assignment).
- **Realistic junk variables:** Looks like legit PowerShell, using believable cmdlets and parameters.
- **Dead code injection:** Includes random try/catch, loops and dummy assignments throughout.
- **Random execution obfuscation:** Obfuscated reconstruction and execution of the final payload.
- **Blend-in obfuscation:** Random whitespace, variable names and syntax constructs enhance stealth.

---

## Example Usage

```bash
python Invoke-Junkpile.py -f ./input.ps1 -o ./output_obfuscated.ps1
```

Or using an inline command:

```bash
python Invoke-Junkpile.py -c "Get-Process | Where-Object { $_.CPU -gt 100 }"
```

With debug output:

```bash
python Invoke-Junkpile.py -f ./input.ps1 -o ./obf.ps1 --debug
```

---

## Output Example (Truncated)

```powershell
$test01 = 6
${Read-Host -ArgumentList -Path \\Backups && ($gstknk)} = "ZSgk";${Compress-Archive -InputFormat -ComputerName $server_ip_09 && ($amicpk)} = "0LCRu";

for ($i = 0; $i -lt 9; $i++) { $nextvar = $i }

$Win32_count = 4

$randIndex = Get-Random -Minimum 2 -Maximum 17
${Expand-Archive -Force -Uri office365.com/?auth=1 && ($kiings)} = "sKSA=";

while ($null) { $run = 9; Start-Sleep -Seconds 6 }

$backupcount = 6
try { $void = Get-Random -Minimum 7 -Maximum 11 } catch { $void = $null }


${Get-ChildItem -ErrorAction SilentlyContinue -LogName Windows PowerShell && ($calran)} = @()
${Get-ChildItem -ErrorAction SilentlyContinue -LogName Windows PowerShell && ($calran)} += @(${Remove-Item -ErrorAction SilentlyContinue -ComputerName $dc_08 && ($eknrb)}, ${Invoke-WebRequest -OutputFormat -LogName Setup && ($egbe)}, ${Write-Output -Force -Name CcmExec && ($bsle)}, ${Write-Host -InputFormat -LogName Application && ($npnpfb)}, ${Restart-Service -Debug -Seconds 10 && ($enfmh)}, ${Read-Host -Debug -Seconds 14 && ($fclclb)}, ${Import-Module -ErrorAction SilentlyContinue -Name powershell && ($gblslr)})

$randIndex = Get-Random -Minimum 0 -Maximum 11

for ($j = 0; $j -lt 0; $j++) { $final += $j }
```

---

## Command-Line Arguments

| Flag              | Description                            |
| ----------------- | -------------------------------------- |
| `-f`, `--file`    | Path to the input PowerShell script    |
| `-c`, `--command` | Inline PowerShell command to obfuscate |
| `-o`, `--output`  | Path to save the obfuscated output     |
| `--debug`         | Enables debug output for development   |

---

## How It Works

**Obfuscation Phase:**

1. **Comment Stripping**: All lines with `#` comments are removed.
2. **Base64 Encoding**: The original PowerShell script is encoded as a single base64 string.
3. **Chunking**: That string is split into randomized-sized segments.
4. **Variable Generation**: Each chunk is assigned to a randomly named variable that mimics legit cmdlet/parameter combos.
5. **Stacking**: Chunks are grouped (typically 2–7 per line) to create the illusion of standard logic flow.
6. **Final Array**: The chunks are combined into an array and then joined into a single base64 string variable.
7. **Execution Line**: The joined base64 is decoded back into the original script using a stealthy and obfuscated `[Text.Encoding]::UTF8.GetString()` expression, which is piped into `IEX`.

**Execution Phase:**

1. PowerShell processes each fake variable assignment.
2. Junk variables and dead code execute without effect.
3. The final base64 string is reconstructed and decoded.
4. The resulting original PowerShell code is executed via `IEX`.

This creates a layered illusion of complexity while keeping the actual behavior intact.

---

## VirusTotal Comparison

The power of obfuscation—visualized. The sample used was the "Using Reflection" script found over at https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell

**Original Script (Unobfuscated AMSI Bypass)**  
This sample was detected by numerous engines: c65416981ba34fbb9638e263585a4ad908705126da79bb8fc353fea90a6824a9

![VirusTotal Detection - Original](assets/vt_1.png)

**Invoke-Junkpile Obfuscated Script**  
After running the same script through Invoke-Junkpile: 3b5602182826d17beeac8ebb204950f6fe4a85809c91e38bd5dff7e46e684167

![VirusTotal Detection - Obfuscated](assets/vt_2.png)

✅ **0 / 63 detections**

> *Heavily obfuscated, yet still fully functional.*

---

## Limitations / Drawbacks

- ❌ Does **not** currently support:
  - Scripts with very large inline binaries or images may not work properly (some did, some didn't)
  - Increases script size.

---

## Use Cases

- Testing SIEM detection logic
- Evading static detection for red team scripts
- Teaching or demonstrating PowerShell obfuscation techniques

---

## Deobfuscation

If you know what to look for, it shouldn't be too bad if you allow the PowerShell interpreter to do most of the work for you. 

1. Identify the variable that gets invoked using PowerShell invoke expressions (iex). It will be near the bottom.
2. Replace the invoke with Write-Host to print the contents of the variable.
3. You'll get Base64 echoed upon script excution. Use your favorite command line utility or online utility such as Cyberchef to decode it.
4. Profit!

---

## To-do
More randomly generated obfuscation around the Base64 execution and invoke expression.
More to come!

---

## Disclaimer

This tool is intended for **educational and research purposes** only. Use responsibly and ethically.
