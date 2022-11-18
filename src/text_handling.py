import re

class Formatter:
    """
    Formats and cleans text, including targeted corrections.
    """

    def remove_nbsp(text):
        # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)
        return text.replace(u'\xa0', ' ').strip()

    def remove_extra_spaces(text):
        return re.sub(r" +", r" ", text)

    def remove_other_notes_bullet(text):
        return re.sub(r"\* Other notes and player tips go here\.*", r"", text)

    def reformat_links(text):
        return re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", text)

    def perform_targeted_corrections(name, text):
        correction = text

        # Would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if name == "Alabaster Lord's Sword":
            correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", text)
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

class Writer:
    """
    Handles writing objects to Obsidian *.md files.
    """