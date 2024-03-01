[**Download this plugin**](https://github.com/oxygen-dioxide/dsinfo/archive/refs/heads/main.zip)

# DsInfo
Show informations about a openutau diffsinger voicebank.

Example:
```
Singer path: E:\repos\OpenUtau\OpenUtau\bin\Release\net6.0-windows\Singers\AIkie_ZH_v1t2_var
===== Acoustic Model =====
Supported expressions: GENC VELC ENE BREC
Use shallow diffusion: True
===== Pitch Model =====
This singer contains pitch model
Use melody encoder: True
Support PEXP: True
===== Duration Model =====
This singer uses DiffSinger variance duration model
```

## Usage
Before using, please [install python](https://www.python.org/downloads/), set python as the default application for opening .py files, and run the following command to install the modules it requires:
```
pip install ruamel.yaml py_linq
```

There are two ways to use this script:
### Use it outside of OpenUtau
Run dsinfo.py and input the path to your DiffSinger voicebank.

### Use it as a plugin from OpenUtau
Place the folder under the "Plugins" folder of your OpenUtau. 

Create a track. Select a DiffSinger voicebank. Create a vocal part. Create a note inside it. Select the note. Run "Batch Edits -> Legacy Plugin (Experimental) -> DiffSinger Voicebank Information"