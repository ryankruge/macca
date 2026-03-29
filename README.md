# MACCA (MAC Spoofing Tool)
MACCA is a CLI MAC spoofing tool. This tool operates using the built-in `ip` command in order to configure the MAC address of network interfaces. By default, executing this tool will generate a random MAC address using the `manuf.json` file that contains thousands of different *Organisationally Unique Identifiers* (OUIs) to mask the identity of the device. The last six bytes of the address are populated at random using an integrated function.
# Application Usage
## Support
This tool only supports Linux due to the foundation of the tool being built upon Linux-exclusive command-line tools.
## Requirements
- Scapy Library
- JSON Library
- RE (Regex) Library
```
python -m pip install ./requirements.txt
```
## Summary
Please consider that altering your MAC address can affect your ability to connect to systems that feature MAC-filtering. The use of this software should be kept within the bounds of local and federal laws and regulations. I will not accept responsibility for any repercussions incurred by such misuse.
