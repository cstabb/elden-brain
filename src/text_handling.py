import re

class Formatter:
    """
    Formats and cleans text, including targeted corrections.
    """

    def condense_newlines(text):
        text = re.sub(r"\n +", r"\n", text)
        return re.sub(r"(\n){2,}", r"\1\1", text)

    def replace_special_characters(text):
        # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)
        text = re.sub(r"[“”]", r'"', text)
        text = re.sub(r"’", r"'", text)
        text = text.replace('\u02cc', ' ')
        text = text.replace('\u032f', ' ')
        text = text.replace('\u2666', ' ')  # Black Diamond
        text = text.replace('\u2193', '')   # Downward Arrow
        text = text.replace('\u2193', 'i')   # Pronunciation I
        text = text.replace('\u2716', 'X')   # Multiplication X
        return text.replace(u'\xa0', ' ').strip()

    def remove_extra_spaces(text):
        return re.sub(r" +", r" ", text)

    def remove_other_notes_bullet(text):
        text = re.sub(r"\* Other notes and player tips go here\.*\n*", r"", text)
        return re.sub(r"\* Other notes & Tips go here\.*\n*", r"", text)

    def remove_hemorrhage_links(text):
        return re.sub(r"\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)", r"", text)

    def remove_video_links(text):
        return re.sub(r"(\* )*\[+Video[^\]]+\]\([^\)]+\)\]*", r"", text)

    def reformat_links(text):
        # return re.sub(r"\[(.+)\]\(\/.+\"Elden Ring (.+)\"\)", r"[[\2|\1]]", text)
        text =  re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", text)
        return re.sub(r"\[([^\[]+\[[0-9]\])\]\(\/[^\[\(]+[\[\(][0-9][\]\)] \"Elden Ring ([^\[\(]+[\[\(][0-9][\]\)])\"\)", r"[[\2|\1]\]", text)

    def remove_builds_header(text):
        return re.sub(r"\#+ Builds", r"", text)

    def unlink_builds(text):
        return re.sub(r"\[\[Builds#[^\|]+\|([^\]]+)\]\]", r"\1", text)

    def unlink_special_weaknesses(text):
        return re.sub(r"\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]", r"\1", text)

    def redirect_ashofwar_skill_links(text):
        return re.sub(r"\[\[Ash of War: ", r"[[", text)

    def reformat_map_links(text):
        return re.sub(r"[\[]+([^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+) \"([^\"]+)\"\)\]*\.*", r"[\1](\1)", text)

    def remove_map_links(text):
        text = re.sub(r"\[+(.+)#.+\|\[[Mm]ore [Ii]nfo *\]\]+", r"", text) # Executioner's Greataxe only?
        text = re.sub(r"\[\[map\]\]\(\/Interactive\+Map\?[^\)]+\)", r"", text) # Executioner's Greataxe only?
        text = re.sub(r"\[\[Map Link\]\]\(\/Interactive\+Map\?[^\)]+\)", r"", text)
        return re.sub(r"\[(Elden Ring [Mm]ap [Hh]ere|Map Coordinates|Map [Ll]ink|Elden Ring [Ii]nteractive [Mm]ap [Ll]ink|Elden Ring Map( [Ll]ink)*)\]\(\1\)", r"", text)

    def remove_notes_after_sell_value(text):
        return re.sub(r"(\* Sell Value: [0-9]+)[\s\S]*", r"\1", text)

    def remove_enemies_table(text):
        return re.sub(r"\| \[\[Creatures and Enemies\|[\s\S]*", r"", text)

    def remove_npcs_table(text):
        return re.sub(r"\| \[\[NPCs\|[\s\S]*", r"", text)

    def remove_locations_table(text):
        return re.sub(r"\| \[\[Locations\|[\s\S]*", r"", text)

    def final_whitespace_cleanup(text):
        text =  re.sub(r" \n", r"\n", text)
        text =  re.sub(r"\n ", r"\n", text)
        text =  re.sub(r"\#+\n", r"\n", text)
        return re.sub(r" \n \n \n", r"\n\n", text)

    def clean_dialogue(text):
        text = re.sub(r"<", r"\<", text)    
        return re.sub(r">", r"\>", text)

    def replace_varre_e(text):
        return re.sub(r"é", r"e", text)

    def unify_boc(text):
        return re.sub(r"\[\[Boc\|Boc\]\]", r"[[Boc the Seamster|Boc the Seamster]]", text)

    def unify_rat(text):
        return re.sub(r"\[\[Rat\|Rat\]\]", r"[[Giant Rat|Giant Rat]]", text)

    def unify_miranda_sprout(text):
        return re.sub(r"\[\[Miranda Flower\|Miranda Flower\]\]", r"[[Miranda Sprout|Miranda Sprout]]", text)

    def unify_giant_miranda_sprout(text):
        return re.sub(r"\[\[Giant Miranda Flower\|Giant Miranda Flower\]\]", r"[[Giant Miranda Sprout|Giant Miranda Sprout]]", text)

    def unify_vulgar_militiamen(text):
        return re.sub(r"\[\[Vulgar Militant\|Vulgar Militant\]\]", r"[[Vulgar Militiamen|Vulgar Militiamen]]", text)

    def reify_bullets(text):
        return re.sub(r"%BULLET%", r"*", text)

    def perform_targeted_corrections(name, text):
        correction = text

        # Would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if name == "Abandoned Cave":
            correction = re.sub(r" See it on the interactive map by clicking on", r"", text)
        if name == "Alabaster Lord's Sword":
            correction = re.sub(r"Sword\*\*\. ", r"Sword. **", text)
            correction = re.sub(r"drop\. \*\*", r"drop.**", correction)
            correction = re.sub(r"Below shows where.*", r"", correction)
            correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", correction)
            correction = Formatter.condense_newlines(correction)
        elif name == "Battle Axe":
            correction = re.sub(r"weapon \n \nCapable", r"weapon*\n\n*Capable", text)
        elif name == "Beast-Repellent Torch":
            correction = re.sub(r"aroma pacifies wild beasts. Torches", r"aroma pacifies wild beasts.*\n\n*Torches", text)
        elif name == "Beast Clergyman":
            correction = re.sub(r"\| \[\[Consumables\|[\s\S]*", r"", text)
        elif name == "Parrying Dagger":
            correction = re.sub(r"PATCHES BELL BEARING", r"Patches' Bell Bearing", text)
        elif name == "Bloodstained Dagger":
            correction = re.sub(r"#gsc\.tab=0", r"", text)
        elif name == "Royal Greatsword":
            correction = re.sub(r"\/\/Strength", r"Strength", text)
        elif name == "Vulgar Militia Saw":
            correction = re.sub(r"\+ \[Example farming route\]\(\/file\/Elden\-Ring\/vulgar\_militia\_saw\.png \"Example farming route\"\)", r"", text)
        elif name == "Flowing Curved Sword":
            correction = re.sub(r" See it on the +\.", r"", text)
        elif name == "Nox Flowing Hammer":
            correction = re.sub(r"\[\[(Flowing Form) \(Nox Flowing Hammer\)", r"[[\1", text)
        elif name == "Varre's Bouquet":
            correction = re.sub(r"é", r"e", text)
        elif name == "Troll's Golden Sword":
            correction = re.sub(r"—", r"--", text)
        elif name == "Zweihander":
            correction = re.sub(r"ä", r"a", text)
        # elif name == "Bolt of Gransax":
        #     correction = re.sub(r"\[\[(Leyndell Royal Capital) \(Legacy Dungeon\)#[^\]]+\]\]", r"[[\1|\1]]", text)
        elif name == "Torch":
            correction = re.sub(r" ### Elden Ring Torch Moveset[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*", r"", text)

        return correction

    def section(header, text, separator="\n", mode='cli'):
        f_string = ""

        if mode == 'cli':
            f_string = f"{header}\n--------\n{text}\n{separator}"
        elif mode == 'file':
            f_string = f"{header}\n--------\n{text}\n{separator}"
            
        return f_string

    def cli_h2(text):
        pass