# Invoke-Junkpile

> Built to execute, not to be understood...

![Invoke-Junkpile Banner](assets/banner.png)

## Overview

**Invoke-Junkpile** is a Python-based tool that takes clean PowerShell scripts and transforms them into an entropic mess of stacked polymorphic variables, junk code, and obfuscated logic through randomization. The generated code is designed to be obfuscated while not appearing obfuscated. Designed for stealth, this tool aims to evade static detection signatures, confuse reverse engineers, and wreak havoc on basic string-matching defenses and entropy checks. In the end, it outputs fully functional, heavily obfuscated PowerShell code.

This was tested on a wide range of PowerShell scripts which worked in 99% of cases (see limitations below). This includes very large and complex scripts and scripts containing assemblies. 

---

## Features

- **Full Script Base64 Encoding**
- **Obfuscated Chunking:** Script is split into chunks assigned to randomly named variables.
- **Chunk Stacking:** Variable groups are randomly joined (2–7 chunks per assignment).
- **Realistic Junk Variables:** Looks like legit PowerShell, using believable cmdlets and parameters.
- **Dead Code Injection:** Includes random try/catch, loops and dummy assignments throughout.
- **Random Execution Obfuscation:** Obfuscated reconstruction and execution of the final payload.
- **Blend-In Obfuscation:** Random whitespace, variable names and syntax constructs enhance stealth.

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
${Get-ChildItem -Verbose -DestinationPath .\Logs && ($tokae)} = "..."
$fragments += ${...}
$payload = $fragments -join ""
[Text.Encoding]::('UT' + 'F8').('Get' + 'Str' + 'ing')([Convert]::('Fr' + 'om' + 'Base64' + 'String')($payload)) | IEX
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

The power of obfuscation—visualized.

**Original Script (Unobfuscated AMSI Bypass)**  
This sample was detected by numerous engines:

![VirusTotal Detection - Original](assets/vt_1.png)

**Invoke-Junkpile Obfuscated Script**  
After running the same script through Invoke-Junkpile:  

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
