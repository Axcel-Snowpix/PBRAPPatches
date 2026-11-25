from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import sys

# Pk4 files have the blocks in ABCD order.
BLOCK_ORDERS: dict[int, str] = {
    0:  "ABCD",
    1:  "ABCD",
    2:  "ABCD",
    3:  "ABCD",
    4:  "ABCD",
    5:  "ABCD",
    6:  "ABCD",
    7:  "ABCD",
    8:  "ABCD",
    9:  "ABCD",
    10: "ABCD",
    11: "ABCD",
    12: "ABCD",
    13: "ABCD",
    14: "ABCD",
    15: "ABCD",
    16: "ABCD",
    17: "ABCD",
    18: "ABCD",
    19: "ABCD",
    20: "ABCD",
    21: "ABCD",
    22: "ABCD",
    23: "ABCD",
}

PBR_ENCODING: defaultdict[str, int] = defaultdict(lambda: 0x00E0, {
    "　": 0x0001,
    **{hiragana: 0x0002 + i for i, hiragana in enumerate("ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでと")},
    **{hiragana: 0x002A + i for i, hiragana in enumerate("どなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをん")},
    **{katakana: 0x0052 + i for i, katakana in enumerate("ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデト")},
    **{katakana: 0x007A + i for i, katakana in enumerate("ドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲン")},
    **{fullwidth_num: 0x00A2 + i for i, fullwidth_num in enumerate("０１２３４５６７８９")},
    **{fullwidth_capital: 0x00AC + i for i, fullwidth_capital in enumerate("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")},
    **{fullwidth_lowercase: 0x00C6 + i for i, fullwidth_lowercase in enumerate("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")},
    **{fullwidth_symbol: 0x00E1 + i for i, fullwidth_symbol in enumerate("！？、。…・／「」『』（）♂♀-＋ー×÷＝～：；．，")},
    **{fullwidth_symbol: 0x00FA + i for i, fullwidth_symbol in enumerate("♠♣♥♦★◎○□△◇＠♪％☀☁☂☃")},
    **{japanese: 0x010B + i for i, japanese in enumerate("㌀㌁㌂㌃㌄㌅㌆円㌇㌈㌉㌊㌋㌌㌍㌎")},
    **{arrow: 0x011B + i for i, arrow in enumerate("←↑↓→▶")},
    "＆": 0x0120,
    **{str(num): 0x0121 + num for num in range(10)},
    **{capital: 0x012B + i for i, capital in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")},
    **{lowercase: 0x0145 + i for i, lowercase in enumerate("abcdefghijklmnopqrstuvwxyz")},
    **{special_capital: 0x15F + i for i, special_capital in enumerate("ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ㌦ØÙÚÛÜÝÞß")},
    **{special_lowercase: 0x17F + i for i, special_lowercase in enumerate("àáâãäåæçèéêëìíîïðñòóôõö㌧øùúûüýþÿ")},
    **{symbol: 0x019F + i for i, symbol in enumerate("ŒœŞşªº")},
    **{fraction: 0x01A5 + i for i, fraction in enumerate("¼½¾")},
    **{symbol: 0x01A8 + i for i, symbol in enumerate("$¡¿!?,.")},
    "㌏": 0x01AF,
    **{symbol: 0x01B0 + i for i, symbol in enumerate("･/‘'“”„«»()")},
    "㌨": 0x01BB,
    "㌩": 0x01BC,
    **{symbol: 0x01BD + i for i, symbol in enumerate("+-*#=&~:;")},
    **{japanese: 0x01C6 + i for i, japanese in enumerate("㌐㌑㌒㌓㌔㌕㌖㌗㌘㌙")},
    "@": 0x01D0,
    "㌚": 0x01D1,
    "%": 0x01D2,
    **{japanese: 0x01D3 + i for i, japanese in enumerate("㌛㌜㌝㌞㌟㌠㌡㌢㌣㌤㌥")},
    " ": 0x01DE,
    "²": 0x01DF,
    **{symbol: 0x01FE + i for i, symbol in enumerate("■▼▽")},
})

PBR_ENCODING_INVERSE: dict[int, str] = {value: key for key, value in PBR_ENCODING.items()}

BLOCK_SIZE = 0x20

@dataclass
class Gen4Pokemon:
    personality_value: int = 0 # int
    # 0-1: skip checksum
    #   2: bad egg
    #  13: pbr bad egg *(see note 1)
    flagsBase: int = 0 # half
    checksum: int = 0 # half

    # Block A
    species: int = 0 # half
    held_item: int = 0 # half
    sid: int = 0 # half
    tid: int = 0 # half
    experience: int = 0 # int
    friendship: int = 0 # byte
    ability: int = 0 # byte
    markings: int = 0 # byte
    language: int = 0 # byte
    hp_ev: int = 0 # byte
    atk_ev: int = 0 # byte
    def_ev: int = 0 # byte
    spe_ev: int = 0 # byte
    spa_ev: int = 0 # byte
    spd_ev: int = 0 # byte
    cool: int = 0 # byte
    beauty: int = 0 # byte
    cute: int = 0 # byte
    smart: int = 0 # byte
    tough: int = 0 # byte
    sheen: int = 0 # byte
    sinnoh_ribbons_1: int = 0 # int

    # Block B
    move1: int = 0 # half
    move2: int = 0 # half
    move3: int = 0 # half
    move4: int = 0 # half
    move1_pp: int = 0 # byte
    move2_pp: int = 0 # byte
    move3_pp: int = 0 # byte
    move4_pp: int = 0 # byte
    ppup_1: int = 0 # byte
    ppup_2: int = 0 # byte
    ppup_3: int = 0 # byte
    ppup_4: int = 0 # byte
    ivs: int = 0 # int, top two bits are flags
    hoenn_ribbons: int = 0 # int
    flagsB: int = 0 # half, fateful/gender/forme/shiny crown
    unusedB: int = 0 # half
    plat_egg_loc: int = 0 # half
    plat_met_loc: int = 0 # half

    # Block C
    nickname: str = "" # 10 halfs + 0xFFFF terminator
    unusedC1: int = 0 # byte
    game_of_origin: int = 0 # byte
    sinnoh_ribbons_2: int = 0 # int
    unusedC2: int = 0 # int

    # Block D
    trainer_name: str = "" # 16 bytes total including an FF terminator
    egg_year: int = 0 # byte
    egg_month: int = 0 # byte
    egg_day: int = 0 # byte
    met_year: int = 0 # byte
    met_month: int = 0 # byte
    met_day: int = 0 # byte
    dp_egg_loc: int = 0 # half
    dp_met_loc: int = 0 # half
    pokerus: int = 0 # byte
    pokeball: int = 0 # byte
    met_level: int = 0 # byte, top bit is OT gender
    encounter_type: int = 0 # byte
    hgss_pokeball: int = 0 # byte
    mood: int = 0 # byte

    def parse_a_block(self, data: bytes) -> None:
        self.species = int.from_bytes(data[0:2], byteorder="little")
        self.held_item = int.from_bytes(data[2:4], byteorder="little")
        self.sid = int.from_bytes(data[4:6], byteorder="little")
        self.tid = int.from_bytes(data[6:8], byteorder="little")
        self.experience = int.from_bytes(data[8:0xC], byteorder="little")
        self.friendship = data[0xC]
        self.ability = data[0xD]
        self.markings = data[0xE]
        self.language = data[0xF]
        self.hp_ev = data[0x10]
        self.atk_ev = data[0x11]
        self.def_ev = data[0x12]
        self.spe_ev = data[0x13]
        self.spa_ev = data[0x14]
        self.spd_ev = data[0x15]
        self.cool = data[0x16]
        self.beauty = data[0x17]
        self.cute = data[0x18]
        self.smart = data[0x19]
        self.tough = data[0x1A]
        self.sheen = data[0x1B]
        self.sinnoh_ribbons_1 = int.from_bytes(data[0x1C:0x20], byteorder="little")

    def build_a_block(self) -> bytes:
        output = bytearray()
        output.extend(self.species.to_bytes(2, byteorder="little"))
        output.extend(self.held_item.to_bytes(2, byteorder="little"))
        output.extend(self.sid.to_bytes(2, byteorder="little"))
        output.extend(self.tid.to_bytes(2, byteorder="little"))
        output.extend(self.experience.to_bytes(4, byteorder="little"))
        output.append(self.friendship)
        output.append(self.ability)
        output.append(self.markings)
        output.append(self.language)
        output.append(self.hp_ev)
        output.append(self.atk_ev)
        output.append(self.def_ev)
        output.append(self.spe_ev)
        output.append(self.spa_ev)
        output.append(self.spd_ev)
        output.append(self.cool)
        output.append(self.beauty)
        output.append(self.cute)
        output.append(self.smart)
        output.append(self.tough)
        output.append(self.sheen)
        output.extend(self.sinnoh_ribbons_1.to_bytes(4, byteorder="little"))

        return bytes(output)

    def parse_b_block(self, data: bytes) -> None:
        self.move1 = int.from_bytes(data[0x0:0x2], byteorder="little")
        self.move2 = int.from_bytes(data[0x2:0x4], byteorder="little")
        self.move3 = int.from_bytes(data[0x4:0x6], byteorder="little")
        self.move4 = int.from_bytes(data[0x6:0x8], byteorder="little")
        self.move1_pp = data[8]
        self.move2_pp = data[9]
        self.move3_pp = data[0xA]
        self.move4_pp = data[0xB]
        self.ppup_1 = data[0xC]
        self.ppup_2 = data[0xD]
        self.ppup_3 = data[0xE]
        self.ppup_4 = data[0xF]
        self.ivs = int.from_bytes(data[0x10:0x14], byteorder="little")
        self.hoenn_ribbons = int.from_bytes(data[0x14:0x18], byteorder="little")
        self.flagsB = int.from_bytes(data[0x18:0x1A], byteorder="little")
        self.unusedB = int.from_bytes(data[0x1A:0x1C], byteorder="little")
        self.plat_egg_loc = int.from_bytes(data[0x1C:0x1E], byteorder="little")
        self.plat_met_loc = int.from_bytes(data[0x1E:0x20], byteorder="little")

    def build_b_block(self) -> bytes:
        output = bytearray()
        output.extend(self.move1.to_bytes(2, byteorder="little"))
        output.extend(self.move2.to_bytes(2, byteorder="little"))
        output.extend(self.move3.to_bytes(2, byteorder="little"))
        output.extend(self.move4.to_bytes(2, byteorder="little"))
        output.append(self.move1_pp)
        output.append(self.move2_pp)
        output.append(self.move3_pp)
        output.append(self.move4_pp)
        output.append(self.ppup_1)
        output.append(self.ppup_2)
        output.append(self.ppup_3)
        output.append(self.ppup_4)
        output.extend(self.ivs.to_bytes(4, byteorder="little"))
        output.extend(self.hoenn_ribbons.to_bytes(4, byteorder="little"))
        output.extend(self.flagsB.to_bytes(2, byteorder="little"))
        output.extend(self.unusedB.to_bytes(2, byteorder="little"))
        output.extend(self.plat_egg_loc.to_bytes(2, byteorder="little"))
        output.extend(self.plat_met_loc.to_bytes(2, byteorder="little"))

        return bytes(output)

    def parse_c_block(self, data: bytes) -> None:
        nickname_bytes = data[:0x16]
        self.nickname = decode_text(nickname_bytes, 11)
        self.unusedC1 = data[0x16]
        self.game_of_origin = data[0x17]
        self.sinnoh_ribbons_2 = int.from_bytes(data[0x18:0x1C], byteorder="little")
        self.unusedC2 = int.from_bytes(data[0x1C:0x20], byteorder="little")

    def build_c_block(self) -> bytes:
        nickname = self.nickname[:10] # trim nickname past 10 characters
        output = bytearray()
        for char in nickname:
            output.extend(PBR_ENCODING[char].to_bytes(2, byteorder="little"))
        output.extend([0xFF, 0xFF])
        output.extend([0] * ((10 - len(nickname)) * 2))
        output.append(self.unusedC1)
        output.append(self.game_of_origin)
        output.extend(self.sinnoh_ribbons_2.to_bytes(4, byteorder="little"))
        output.extend(self.unusedC2.to_bytes(4, byteorder="little"))

        return bytes(output)

    def parse_d_block(self, data: bytes) -> None:
        trainer_bytes = data[:0x10]
        self.trainer_name = decode_text(trainer_bytes, 8)
        self.egg_year = data[0x10]
        self.egg_month = data[0x11]
        self.egg_day = data[0x12]
        self.met_year = data[0x13]
        self.met_month = data[0x14]
        self.met_day = data[0x15]
        self.dp_egg_loc = int.from_bytes(data[0x16:0x18], byteorder="little")
        self.dp_met_loc = int.from_bytes(data[0x18:0x1A], byteorder="little")
        self.pokerus = data[0x1A]
        self.pokeball = data[0x1B]
        self.met_level = data[0x1C]
        self.encounter_type = data[0x1D]
        self.hgss_pokeball = data[0x1E]
        self.mood = data[0x1F]

    def build_d_block(self) -> bytes:
        trainer_name = self.trainer_name[:7]
        output = bytearray()
        for char in trainer_name:
            output.extend(PBR_ENCODING[char].to_bytes(2, byteorder="little"))
        output.extend([0xFF, 0xFF])
        output.extend([0] * ((7 - len(trainer_name)) * 2))
        output.append(self.egg_year)
        output.append(self.egg_month)
        output.append(self.egg_day)
        output.append(self.met_year)
        output.append(self.met_month)
        output.append(self.met_day)
        output.extend(self.dp_egg_loc.to_bytes(2, byteorder="little"))
        output.extend(self.dp_met_loc.to_bytes(2, byteorder="little"))
        output.append(self.pokerus)
        output.append(self.pokeball)
        output.append(self.met_level)
        output.append(self.encounter_type)
        output.append(self.hgss_pokeball)
        output.append(self.mood)

        return bytes(output)

    @classmethod
    def create_from_binary(cls, data: bytes) -> Gen4Pokemon:
        mon = Gen4Pokemon()
        mon.personality_value = int.from_bytes(data[0x0:0x4], byteorder="little")
        mon.flagsBase = int.from_bytes(data[0x4:0x6], byteorder="little")
        mon.checksum = int.from_bytes(data[0x6:0x8], byteorder="little")

        block_functions = {
            "A": mon.parse_a_block,
            "B": mon.parse_b_block,
            "C": mon.parse_c_block,
            "D": mon.parse_d_block,
        }

        blocks = [data[0x8 + (i*0x20):0x28 + (0x20*i)] for i in range(4)]
        block_shuffle = BLOCK_ORDERS[((mon.personality_value & 0x3E000) >> 0xD) % 24]
        for i, block in enumerate(blocks):
            block_functions[block_shuffle[i]](block)

        return mon

    # TODO: Make the below line not so long.
    def __repr__(self):
        return f"\t{self.species}: " "{'name': '" f"{self.nickname}', 'pid': {self.personality_value}, 'exp': {self.experience}, 'form': {(self.flagsB & 0b11111000) >> 3}, 'ivs': {self.ivs & 0x3FFFFFFF}, 'item': {self.held_item}, 'hp_ev': {self.hp_ev}, 'atk_ev': {self.atk_ev}, 'def_ev': {self.def_ev}, 'spe_ev': {self.spe_ev}, 'spa_ev': {self.spa_ev}, 'spd_ev': {self.spd_ev}" "}," 
    
    def __eq__(self, other):
        return self.species == other.species

    def __lt__(self, other):
        return self.species < other.species

def decode_text(text: bytes, text_length: int) -> str:
    decoded_text = ""
    for i in range(text_length):
        char = int.from_bytes(text[(i*2):(i*2)+2], byteorder="little")
        if char == 0xFFFF or char == 0x00:
            break
        decoded_text += PBR_ENCODING_INVERSE[char]
    return decoded_text

# Note 1: PBR also double checks the validity of Pokemon copied from games;
# however, instead of actually setting the bad_egg flag, it sets bit 0xD.

def main():
    if (len(sys.argv) <= 2):
        return
    
    generated_file_name = sys.argv[1]
    pk4_file_names = sys.argv[2:]
    pokemon_list = []
    
    for pk4_file_name in pk4_file_names:
        pk4_file = open(pk4_file_name, "rb")
        pokemon_list.append(Gen4Pokemon.create_from_binary(pk4_file.read(0x88)))
        pk4_file.close()
    
    pokemon_list.sort()
    
    generated_file = open(generated_file_name + ".py", "w")
    generated_file.write(generated_file_name + ": dict[int, dict[str, Any]] = {\n")
    for pkmn in pokemon_list:
        generated_file.write(str(pkmn) + "\n")
    generated_file.write("}")
    generated_file.close()
    
if __name__ == "__main__":
    main()