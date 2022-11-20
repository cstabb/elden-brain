import re

class Formatter:
    """
    Formats and cleans text, including targeted corrections.
    """

    def condense_newlines(text):
        return re.sub(r"(\s){3,}", r"\1\1", text)

    def remove_nbsp(text):
        # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)
        return text.replace(u'\xa0', ' ').strip()

    def remove_extra_spaces(text):
        return re.sub(r" +", r" ", text)

    def remove_other_notes_bullet(text):
        return re.sub(r"\* Other notes and player tips go here\.*", r"", text)

    def remove_hemorrhage_links(text):
        return re.sub(r"\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)", r"", text)

    def remove_video_links(text):
        return re.sub(r"\* \[Video[^\]]+\]\([^\)]+\)", r"", text)

    def reformat_links(text):
        return re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", text)

    def unlink_builds(text):
        return re.sub(r"\[\[Builds#[^\|]+\|([^\]]+)\]\]", r"\1", text)

    def unlink_special_weaknesses(text):
        return re.sub(r"\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]", r"\1", text)

    def redirect_ashofwar_skill_links(text):
        return re.sub(r"\[\[Ash of War: ", r"[[", text)

    def reformat_map_links(text):
        return re.sub(r"[\[]+([^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+) \"([^\"]+)\"\)\]*\.*", r"[\1](\1)", text)

    def remove_map_links(text):
        return re.sub(r"\[(Elden Ring Map here|Map Coordinates|Map [Ll]ink|Elden Ring Map( [Ll]ink)*)\]\(\1\)", r"", text)

    def perform_targeted_corrections(name, text):
        correction = text

        # Would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if name == "Alabaster Lord's Sword":
            correction = re.sub(r"Sword\*\*\. ", r"Sword. **", text)
            correction = re.sub(r"drop\. \*\*", r"drop.**", correction)
            correction = re.sub(r"Below shows where.*", r"", correction)
            correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", correction)
            correction = Formatter.condense_newlines(correction)
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
        # elif name == "Bolt of Gransax":
        #     correction = re.sub(r"\[\[(Leyndell Royal Capital) \(Legacy Dungeon\)#[^\]]+\]\]", r"[[\1|\1]]", text)
        elif name == "Torch":
            #[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*
            correction = re.sub(r" ### Elden Ring Torch Moveset[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*", r"", text)
            #correction = re.sub(r"\n\n", r"\n", correction)
        # print(text)
        # print('-----------------')
        # print(correction)
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