import os
import re
from enum import Enum

import markdownify as md

from constants import *
from text_handling import Formatter

class Entity:
    def __init__(self, name, url='', category=None, image=None, header='', description='', location='', use='', notes=''):
        self.name = name
        self.url = url
        self.category = category
        self.image = image
        #TODO: assert type is EntityType before assignment
        self.header = self.format_links(md(header, strip=["img"])) # Initial description paragraph
        self.description = self.format_links(md(description, strip=["img"]))
        self.location = self.format_links(md(location, strip=["img"]))
        self.use = self.format_links(md(use, strip=["img"]))
        self.notes = self.format_links(md(notes, strip=["img"]))

    def __str__(self):
        name_f_string = f"\n{self.name}\n\
========\n\n"

        description_f_string = f"DESCRIPTION\n\
--------\n\
{self.description}\n\n"

        location_f_string = ''
        if self.location != '':
            location_f_string = f"LOCATION\n\
--------\n\
{self.location}\n\n"

        use_f_string = ''
        if self.use != '':
            use_f_string = f"USE\n\
--------\n\
{self.use}\n\n"

        notes_f_string = ''
        if self.notes != '':
            notes_f_string = f"NOTES & TIPS\n\
--------\n\
{self.notes}\n"

        return name_f_string + description_f_string + location_f_string + use_f_string + notes_f_string

    def perform_targeted_corrections(self, text=""):

        # would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if self.category == 'Weapons':
            if self.name == "Alabaster Lord's Sword":
                correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", text)
            elif self.name == "Parrying Dagger":
                correction = re.sub(r"PATCHES BELL BEARING", r"Patches' Bell Bearing", text)
            elif self.name == "Bloodstained Dagger":
                correction = re.sub(r"#gsc\.tab=0", r"", text)
            elif self.name == "Royal Greatsword":
                correction = re.sub(r"\/\/Strength", r"Strength", text)
            elif self.name == "Vulgar Militia Saw":
                correction = re.sub(r"\+ \[Example farming route\]\(\/file\/Elden\-Ring\/vulgar\_militia\_saw\.png \"Example farming route\"\)", r"", text)
            elif self.name == "Flowing Curved Sword":
                correction = re.sub(r" See it on the +\.", r"", text)
            elif self.name == "Nox Flowing Hammer":
                correction = re.sub(r"\[\[(Flowing Form) \(Nox Flowing Hammer\)", r"[[\1", text)
            # elif self.name == "Bolt of Gransax":
            #     correction = re.sub(r"\[\[(Leyndell Royal Capital) \(Legacy Dungeon\)#[^\]]+\]\]", r"[[\1|\1]]", text)
            elif self.name == "Torch":
                #[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*
                correction = re.sub(r" ### Elden Ring Torch Moveset[\'\,\"\/\(\)\+ \.\|\[\]#\*\w\&\n]*", r"", text)
                #correction = re.sub(r"\n\n", r"\n", correction)

        return correction

    def format_links(self, md_text):
        md_text_whitespace_fixed = md_text.replace(u'\xa0', ' ').strip() # Remove leading and trailing whitespace, and non-breaking spaces (&nbsp;)

        # Removals
        rx_hemorrhage = re.sub(r"\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)", "", md_text_whitespace_fixed)
        rx_remove_video_links = re.sub(r"\[Video[^\]]+\]\([^\)]+\)", "", rx_hemorrhage)

        # Reformatting
        rx_map_links = re.sub(r"[\[]+([^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+) \"([^\"]+)\"\)\]*\.*", r"[\1](\1)", rx_remove_video_links) # Fix map links
        # Now that all map links are in the same format, remove the generic ones i.e. not those that point toward a specific entity or location ("Elden Ring Map here", "Map Link", etc.)
        rx_remove_map_links = re.sub(r"\[(Elden Ring Map here|Map Coordinates|Map [Ll]ink|Elden Ring Map( [Ll]ink)*)\]\(\1\)", r"", rx_map_links)
        rx_links = re.sub(r"\[([^]]+)\]\(\/([^?\[\]]+) \"Elden Ring ([^\[\]]+)\"\)", r"[[\3|\1]]", rx_remove_map_links) # Reformat links
        
        # Due diligence
        rx_other_notes = re.sub(r"Other notes and player tips go here\.*", r"", rx_links)
        rx_unlink_builds = re.sub(r"\[\[Builds#[^\|]+\|([^\]]+)\]\]", r"\1", rx_other_notes)
        rx_special_weaknesses = re.sub(r"\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]", r"\1", rx_unlink_builds)
        rx_ash_of_war_skill_links = re.sub(r"\[\[Ash of War: ", r"[[", rx_special_weaknesses)
        rx_condense_multispaces = re.sub(r" +", r" ", rx_ash_of_war_skill_links) # Condense multiple spaces

        corrections_applied = self.perform_targeted_corrections(rx_condense_multispaces)

        return corrections_applied

    def set_location(self, location_in_html):
        self.location = md(location_in_html.strip().replace(u'\xa0', ' '))

    def write(self, additional_tags=[], filename=None):

        if filename is None:
            filename = self.name

        path = LOCAL_CACHE + LOCAL_VAULT_NAME
        if self.category is not None:
            path += self.category.value + "/"
        # Create destination directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)

        f = open(path + filename+'.md', 'w')
        
        tags_md_string = ""
        # Front matter formatting--works, but ugly!
        # if additional_tags == []:
        #     additional_tags = ""
        # else:
        #     additional_tags = "\n- " + "\n- ".join(additional_tags)
        # tags_md_string = f"---\ntags:\n- {self.category.value}{additional_tags}\n---\n\n"
        if self.category is not None:
            category_string = re.sub(r" +", r"", self.category.value)
            tags_md_string = f"#{category_string}\n\n"

        image = ""
        if self.image is not None:
            image = "![["+self.image.url.split("/")[-1]+"]]\n"
        
        description_md_string = ""
        if self.description != "":
            description_md_string = f"## Description\n\n{self.description}\n\n"

        location_md_string = ""
        if self.location != "":
            location_md_string = f"## Location\n\n{self.location}\n\n"

        use_md_string = ""
        if self.use != "":
            use_md_string = f"## Use\n\n{self.use}\n\n"

        notes_md_string = ""
        if self.notes != "":
            notes_md_string = f"## Notes & Tips\n\n{self.notes}\n\n"

        output_str = tags_md_string + image + description_md_string + location_md_string + use_md_string + notes_md_string
        
        f.write(output_str)
        f.close()

class Image:
    def __init__(self, data, name=''):
        self.data = data
        self.name = name
    
    def write(self, path=None):
        """
        Write image out to file.
        """
        destination_path = ''
        if path is not None:
            destination_path = path
        else:
            destination_path = LOCAL_CACHE + LOCAL_VAULT_NAME + LOCAL_ASSETS + self.name
        
        with open(destination_path, 'wb') as handler:
            handler.write(self.data)

class Dialogue:
    def __init__(self, context, line):
        self.context = context
        self.line = line

    def __str__(self):
        rep_str = "{}\n{}\n{}".format(self.name, self.type, self.description)
        #print(rep_str, self.name, self.type, self.description)
        return f'{self.name}\n{self.description}'
        
class NPC(Entity):
    def __init__(self, name, url='', type='', header='', notes='', location='', dialogue=''):
        super().__init__(url, name, type, header, notes)
        self.location = location
        self.dialogue = dialogue
