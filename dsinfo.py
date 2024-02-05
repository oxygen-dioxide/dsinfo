import sys
import yaml
from   typing   import List, Tuple, Dict, Optional
import pathlib
from   py_linq  import Enumerable

def GetSingerPath(tmpFile:pathlib.Path) -> Optional[pathlib.Path]:
    with tmpFile.open("r", encoding="utf-8") as f:
        line = Enumerable(f)\
            .select(lambda x: x.strip())\
            .where(lambda x: x.startswith("VoiceDir="))\
            .first()
        if(line is None):
            return None
        return pathlib.Path(line[9:])

if(len(sys.argv) == 1):
    print("Please input the path of your diffsinger voicebank")
    path = pathlib.Path(input().strip())
else:
    path = pathlib.Path(sys.argv[1])
singerPath = path
if(path.is_file()):
    if(path.suffix.lower() == ".ust" or path.suffix.lower() == ".tmp"):
        singerPath = GetSingerPath(path)
        if(singerPath is None):
            print(f"Please select a singer in OpenUtau first.")
            input("Press Enter to exit")
            exit(1)
    else:
        singerPath = path.parent
elif(not path.is_dir()):
    print(f"Error: {path} is not a file or directory")
    input("\nPress Enter to exit")
    exit(1)

print("Singer path:", singerPath)

if(not (singerPath / "dsconfig.yaml").is_file()):
    print(f"Error: {singerPath} is not a DiffSinger voicebank")
    input("\nPress Enter to exit")
    exit(1)

characterYaml = {
    "subbanks" : []
}
if((singerPath / "character.yaml").is_file()):
    characterYaml.update(yaml.safe_load((singerPath / "character.yaml").open("r", encoding="utf-8")))
    if("subbanks" in characterYaml and isinstance(characterYaml["subbanks"], list) and len(characterYaml["subbanks"]) > 0):
        subbankNames = Enumerable(characterYaml["subbanks"]).select(lambda x: x["color"]).to_list()
        print(f"Voice colors: {' '.join(subbankNames)}")
        
print("===== Acoustic Model =====")
supportedExpressions:List[str] = []
#default values
acousticConfig = {
    "use_key_shift_embed": False,
    "use_speed_embed":False,
    "use_energy_embed":False,
    "use_breathiness_embed":False,
    "use_shallow_diffusion":False,
}
acousticConfig.update(yaml.safe_load((singerPath / "dsconfig.yaml").open("r", encoding="utf-8")))
supportedExpressions = \
    acousticConfig["use_key_shift_embed"] * ["GENC"] + \
    acousticConfig["use_speed_embed"] * ["VELC"] + \
    acousticConfig["use_energy_embed"] * ["ENE"] + \
    acousticConfig["use_breathiness_embed"] * ["BREC"]
print(f"Supported expressions: {' '.join(supportedExpressions)}")
print(f"Use shallow diffusion: {acousticConfig['use_shallow_diffusion']}")

print("===== Pitch Model =====")
pitchConfig = {
    "pitch": None,
    "use_note_rest": False,
    "use_expr": False,
}
if((singerPath / "dspitch" / "dsconfig.yaml").is_file()):
    pitchPath = singerPath / "dspitch"
else:
    pitchPath = singerPath
pitchConfig.update(yaml.safe_load((pitchPath / "dsconfig.yaml").open("r", encoding="utf-8")))
if(pitchConfig["pitch"] is None):
    print("This singer does not contain pitch model")
else:
    print("This singer contains pitch model")
    print(f"Use melody encoder: {pitchConfig['use_note_rest']}")
    print(f"Support PEXP: {pitchConfig['use_expr']}")

print("===== Duration Model =====")
durConfig = {
    "dur": None,
}
if((singerPath / "dsdur" / "dsconfig.yaml").is_file()):
    durPath = singerPath / "dsdur"
else:
    durPath = singerPath
durConfig.update(yaml.safe_load((durPath / "dsconfig.yaml").open("r", encoding="utf-8")))
if(durConfig["dur"] is None):
    print("This singer does not use DiffSinger variance duration model")
else:
    print("This singer uses DiffSinger variance duration model")

input("\nPress Enter to exit")