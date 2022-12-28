import re

class Formatter:
    '''
    Formats and cleans text, including targeted corrections.
    '''

    def applyPreMarkdownFixes(text):
        text = re.sub(r'\<p\>[\s]+\<\/p\>', r'', text)
        text = re.sub(r'<br\/>', r'<br>', text)
        return text

    def applyCharacterFixes(markdown):
        markdown = Formatter.replace_special_characters(markdown)

        return markdown

    def applyTextFixes(markdown):
        """
        Apply all of the little text fixes for inconsistencies, misspellings, standardizing, 
        or just plain beautification.

        Order matters here, unfortunately, so those changes with the most far-ranging
        impact (such as initial link cleanup and standardization) come first.
        """
        ## Essential cleanup
        markdown = Formatter.prep_map_links(markdown)
        markdown = Formatter.reformat_links(markdown)
        markdown = Formatter.remove_more_info_links(markdown)
        markdown = Formatter.remove_map_links(markdown)
        markdown = Formatter.map_link_cleanup(markdown)
        markdown = Formatter.remove_video_links(markdown)
        markdown = Formatter.remove_image_links(markdown)
        markdown = Formatter.remove_elden_ring_links(markdown)
        markdown = Formatter.fix_brackets_in_item_names(markdown)
        markdown = Formatter.remove_other_notes_bullet(markdown)
        markdown = Formatter.fix_accented_e(markdown)
        markdown = Formatter.reformat_notes(markdown)

        ## Unify inconsistent links/names
        markdown = Formatter.unify_d(markdown)
        markdown = Formatter.unify_enia(markdown)
        markdown = Formatter.unify_ensha(markdown)
        markdown = Formatter.unify_ranni(markdown)
        markdown = Formatter.unify_gideon_boss(markdown)
        markdown = Formatter.unify_hewg(markdown)
        markdown = Formatter.unify_hoslow(markdown)
        markdown = Formatter.unify_iji(markdown)
        markdown = Formatter.unify_godfrey(markdown)
        markdown = Formatter.unify_gurranq(markdown)
        markdown = Formatter.unify_malenia(markdown)
        markdown = Formatter.unify_miriel(markdown)
        markdown = Formatter.unify_morgott(markdown)
        markdown = Formatter.unify_seluvis(markdown)
        markdown = Formatter.unify_varre(markdown)
        markdown = Formatter.unify_renalla(markdown)
        markdown = Formatter.unify_torrent(markdown)
        markdown = Formatter.unify_bernahl(markdown)
        markdown = Formatter.unify_nomadic_merchant_west_liurnia(markdown)
        markdown = Formatter.unify_hermit_merchant_mountaintops_east(markdown)
        markdown = Formatter.unify_alexander(markdown)
        markdown = Formatter.unify_boc(markdown)
        markdown = Formatter.unify_imp(markdown)
        # Enemies
        markdown = Formatter.unify_astel(markdown)
        markdown = Formatter.unify_putrid_corpse(markdown)
        markdown = Formatter.unify_moongrum(markdown)
        markdown = Formatter.unify_rat(markdown)
        markdown = Formatter.unify_monstrous_crow(markdown)
        markdown = Formatter.unify_monstrous_dog(markdown)
        markdown = Formatter.unify_wolf(markdown)
        markdown = Formatter.unify_kindred(markdown)
        markdown = Formatter.unify_miranda_sprout(markdown)
        markdown = Formatter.unify_giant_miranda_sprout(markdown)
        # Locations
        markdown = Formatter.unify_swamp_of_aeonia(markdown)
        markdown = Formatter.unify_war_dead_catacombs(markdown)
        markdown = Formatter.unify_mausoleums(markdown)
        markdown = Formatter.unify_stargazers_ruins(markdown)
        markdown = Formatter.unify_elphael(markdown)
        markdown = Formatter.unify_leyndell(markdown)
        markdown = Formatter.unify_leyndell_ashen_capital(markdown)
        markdown = Formatter.unify_ordina(markdown)
        markdown = Formatter.unify_gelmir(markdown)
        markdown = Formatter.unify_raya_lucaria(markdown)
        markdown = Formatter.unify_liurnia(markdown)
        markdown = Formatter.unify_sellia(markdown)
        markdown = Formatter.unify_shaded_castle(markdown)
        # Weapons/Armor/Spells
        markdown = Formatter.unify_sword_of_st_trina(markdown)
        markdown = Formatter.unify_flame_spells(markdown)
        # Skills
        markdown = Formatter.unify_skills(markdown)

        ## Misc
        markdown = Formatter.unlink_builds(markdown)
        markdown = Formatter.unlink_special_weaknesses(markdown)
        markdown = Formatter.correct_crucible_aspect_spell_names(markdown)
        markdown = Formatter.redirect_ashofwar_skill_links(markdown)

        ## Reify custom fill-ins
        markdown = Formatter.reify_bullets(markdown)

        ## Mostly optional, but annoying, fluff
        markdown = Formatter.suppress_patch_notes(markdown)
        markdown = Formatter.remove_category_links_table(markdown)
        markdown = Formatter.fix_links_inside_tables(markdown)
        markdown = Formatter.add_headers_to_tables(markdown)
        markdown = Formatter.remove_elden_ring_links(markdown)

        ## Final clean-up
        markdown = Formatter.remove_floating_bullets(markdown)
        markdown = Formatter.condense_multiple_spaces(markdown)
        markdown = Formatter.condense_newlines(markdown)
        markdown = Formatter.remove_empty_notes(markdown)
        
        return markdown

    ## Pre-Markdown formatting functions
    # Not necessary so far, but you never know

    ## Post-Markdown formatting functions
    def prep_map_links(text):
        """
        [[Elden Ring Map here](/Interactive+Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA "Elden Ring Interactive Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA")]
        [Elden Ring Map here](/Interactive+Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA "Elden Ring Interactive Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA")
        """
        return re.sub(r'\[(\[[^\]]+\]\([^\)]+\))\]', r'\1', text)

    def reformat_links(text):
        """
        [Elden Ring Map here](/Interactive+Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA "Elden Ring Interactive Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA")
        [[Interactive Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA|Elden Ring Map here]]

        [Leyndell, Royal Capital](/Leyndell,+Royal+Capital "Elden Ring Leyndell, Royal Capital")
        [[Leyndell, Royal Capital|Leyndell, Royal Capital]]

        [Commoner's Headband (Altered)](/Commoner's+Headband+(Altered) "Elden Ring Commoner's Headband (Altered)")
        [[Commoner's Headband (Altered)|Commoner's Headband (Altered)]]
        """
        text = re.sub(r'\[([^\]]+)\]\(\/([^ ]+) \"[^\"]+\"\)', r'[[\2|\1]]', text)
        text = re.sub(r'\+', r' ', text) # Removes ALL +'s... may need something more targeted here
        return text

    def remove_more_info_links(text):
        """
        [[Margit, The Fell Omen#capital-outskirts|More Info]]
        """
        text = re.sub(r'\[\[[^\|]+\|[Mm]ore [Ii]nfo *\]\]', r'', text)
        return text

    def remove_map_links(text):
        """
        [[Interactive Map?id=6861&lat=-88.11&lng=64.93&zoom=8&code=mapA|Elden Ring Map here]]
        """
        text = re.sub(r'\[\[[Ii]nteractive [Mm]ap\?[^\]]+\]\]', r'', text)
        return text

    def map_link_cleanup(text):
        """
         See it on the .
        """
        text = re.sub(r' *See it on the +\.', r'', text)
        return text

    def suppress_patch_notes(text):
        """
        * Updated to patch **1.07**. See [[Patch Notes|Patch Notes]] for details.
        """
        text = re.sub(r'.*[Pp]atch (\*\*)*1\.04(\*\*)*.*', r'', text)
        text = re.sub(r'.*[Pp]atch (\*\*)*1\.041(\*\*)*.*', r'', text)
        text = re.sub(r'.*[Pp]atch (\*\*)*1\.07(\*\*)*.*', r'', text)
        text = re.sub(r'.*[Pp]atch (\*\*)*1\.08(\*\*)*.*', r'', text)
        return text

    def remove_floating_bullets(text):
        text = re.sub(r'\* \n', r'\n', text)
        return text

    def condense_multiple_spaces(text):
        text = re.sub(r' {2,}', r' ', text)
        return text

    def remove_empty_notes(text):
        text = re.sub(r'\n## Notes\n\n$', r'', text)
        return text

    def condense_newlines(text):
        text = re.sub(r'\n +', r'\n', text)
        return re.sub(r'(\n){2,}', r'\1\1', text)

    def replace_special_characters(text):
        text = re.sub(r'[“”]', r'"', text)
        text = re.sub(r'’', r"'", text)
        text = text.replace('%27', "'")
        text = text.replace('\u02cc', ' ')
        text = text.replace('\u032f', ' ')
        text = text.replace('\u2666', '')  # Black Diamond
        text = text.replace('\u2193', '')   # Downward Arrow
        text = text.replace('\u2193', 'i')  # Pronunciation I
        text = text.replace('\u2716', 'X')  # Multiplication X
        text = text.replace('\u221e', '')  # Infinity
        text = text.replace('\u2191', '')  # Upwards Arrow
        text = text.replace('\u2192', '->')  # Rightwards Arrow
        text = text.replace('\u2b58', 'O')  # Heavy Circle
        text = text.replace('\u25b3', 'O')  # White Up-Pointing Triangle
        text = text.replace('\u21d2', '->>')  # Rightward Double Arrow
        text = text.replace('\u2aab', '>')  # Larger Than
        text = text.replace('\u2264', '<=')  # Less Than Or Equal To
        text = text.replace('\u2026', '...')  # Ellipsis
        text = text.replace('\u230a', '')  # Left Floor
        text = text.replace('\u230b', '')  # Right Floor
        text = text.replace('\u00a0', ' ') 
        text = text.replace('\u00e9', 'é') # é=taken from printed output
        text = text.replace(u'\xa0', ' ')
        text = text.replace('é', 'e')
        text = text.replace('é', 'e')
        return text.strip()

    def remove_extra_spaces(text):
        return re.sub(r' +', r' ', text)

    def remove_other_notes_bullet(text):
        text = re.sub(r'.*[Nn]otes (&|and) ([Pp]layer )*([Tt]ips|[Tt]rivia).*', r'', text)
        return text

    def remove_hemorrhage_links(text):
        return re.sub(r'\[\([0-9]+\)\]\(\/Hemorrhage[^\)]+\)', r'', text)

    def remove_video_links(text):
        return re.sub(r'(\* )*\[+Video[^\]]+\]\([^\)]+\)\]*', r'', text)

    def remove_image_links(text):
        return re.sub(r'\[\[[^\|]+\|(.+) \(click for image\)\]\]', r'\1', text)

    # TODO: Revisit to make sure this isn't de-linking Great Runes pages
    def remove_elden_ring_links(text):
        return re.sub(r'\[\[([^\|]+)\|Elden Ring\]\]', r'Elden Ring', text)
    
    def remove_remaining_links(text):
        text = re.sub(r'\[here\]\(here\)', r'', text)
        text = re.sub(r'\[\[Interactive Map|(Minor Erdtrees)\]\]', r'\1', text)
        text = re.sub(r'\[\[Interactive Map\|\[.+(\])+', r'', text)
        return text

    def fix_brackets_in_item_names(text):
        text = re.sub(r'\[([0-9]{1,2})\]', r'(\1)', text) # Replace bracketed numbers with parentheses (for numbered materials)
        return text
    
    # def reformat_links(text):
    #     text = re.sub(r'\[([0-9]{1,2})\]', r'(\1)', text) # Replace bracketed numbers with parentheses (for numbered materials)
    #     text =  re.sub(r'\[([^]]+(\([0-9]{1,2}\))*)\]\(\/([^?\[\]]+) \'Elden Ring ([^\']+)\'\)', r'[[\4|\1]]', text)
    #     return text
    
    def remove_builds_header(text):
        return re.sub(r'\#+ Builds', r'', text)

    def unlink_builds(text):
        return re.sub(r'\[\[Builds#[^\|]+\|([^\]]+)\]\]', r'\1', text)

    def unlink_special_weaknesses(text):
        return re.sub(r'\[\[Special Weaknesses#[^\]]+\|([^\]]+)\]\]', r'\1', text)

    def redirect_ashofwar_skill_links(text):
        return re.sub(r'\[\[Ash of War: ', r'[[', text)

    def correct_crucible_aspect_spell_names(text):
        return re.sub(r'Aspect(s)* of the Crucible:', r'Aspects of the Crucible -', text)

    def reformat_map_links(text):
        return re.sub(r'[\[]+([^\]]+)\]\((\/[I|i]nteractive\+[M|m]ap\?[^\ ]+) \'([^\']+)\'\)\]*\.*', r'[\1](\1)', text)
    
    def remove_anchor_links(text):
        return re.sub(r'(.+)( \[\[.+#[^\|]+\|\[More [Ii]nfo *\]\]\])', r'\1', text)

    def removeNotesAfterSellValue(text):
        return re.sub(r'(\* Sell Value: [0-9]+)[\s\S]*', r'\1', text)

    def fix_accented_e(text):
        return re.sub(r'%C3%A9', r'e', text)

    def fix_links_inside_tables(text):
        text = re.sub(r'(\[\[[^\|]+)(\|)([^\|]+\|)', r'\1\\|\3', text)
        text = re.sub(r'(Defeat .+)(\|)(.+\]\] \|)', r'\1\\|\3', text)
        text = re.sub(r'(At the end of .+)(\|)(.+\]\].+ \|)', r'\1\\|\3', text)
        return text

    def remove_category_links_table(text):
        text = re.sub(r'\| (\*)*\[.+\]\(.+\) \|\n\| --- \|\n\| .+ \|', r'', text)
        text = re.sub(r'\| (\*)*\[\[.+\|.+\]\](\*)* \|\n\| --- \|\n\| .+ \|', r'', text)
        return text
    
    def add_headers_to_tables(text):
        rx = r'(\| (.+) \|\n)(\| [\s\S]*\n\n)'
        table_match = re.search(rx, text)
        try:
            num_pipes = len(re.findall(r'\|', table_match.group(1))) - 1    # Subtract the last pipe

            header1 = ''
            header2 = ''
            for i in range(num_pipes):
                header1 += '| '
                header2 += '| --- '
            header1 += '|\n'
            header2 += '|\n'

            return re.sub(rx, header1 + header2 + r'\1\3', text)
        except:
            return text

    def final_whitespace_cleanup(text):
        text =  re.sub(r' \n', r'\n', text)
        text =  re.sub(r'\n ', r'\n', text)
        text =  re.sub(r'\#+\n', r'\n', text)
        return re.sub(r' \n \n \n', r'\n\n', text)

    def cleanDialogue(text):
        text = re.sub(r'<', r'\<', text)    
        return re.sub(r'>', r'\>', text)

    def unify_varre(text):
        return re.sub(r'Varré', r'Varre', text)

    def unify_sellia(text):
        return re.sub(r'\[\[Sellia\|(.+)\]\]', r'[[Sellia, Town of Sorcery|\1]]', text)
    
    def unify_astel(text):
        return re.sub(r'\[\[Astel Naturalborn of the Void\|(.+)\]\]', r'[[Astel, Naturalborn of the Void|\1]]', text)

    def unify_flame_spells(text):
        text = re.sub(r'\[\[Flame,* Grant [Mm]e Strength\|(.+)\]\]', r'[[Flame, Grant Me Strength|Flame, Grant Me Strength]]', text)
        text = re.sub(r'\[\[Flame,* Fall Upon Them\|(.+)\]\]', r'[[Flame, Fall Upon Them|Flame, Fall Upon Them]]', text)
        text = re.sub(r'\[\[Flame,* Protect Me\|(.+)\]\]', r'[[Flame, Protect Me|Flame, Protect Me]]', text)
        text = re.sub(r'\[\[Flame,* Cleanse Me\|(.+)\]\]', r'[[Flame, Cleanse Me|Flame, Cleanse Me]]', text)
        text = re.sub(r'\[\[Surge,* O Flame!*\|(.+)\]\]', r'[[Surge, O Flame!|Surge, O Flame!]]', text)
        text = re.sub(r'\[\[Burn,* O Flame!*\|(.+)\]\]', r'[[Burn, O Flame!|Burn, O Flame!]]', text)
        text = re.sub(r'\[\[Whirl,* O Flame!*\|(.+)\]\]', r'[[Whirl, O Flame!|Whirl, O Flame!]]', text)
        text = re.sub(r'\[\[O,* Flame!*\|(.+)\]\]', r'[[O, Flame!|O, Flame!]]', text)
        return text
    
    def unify_alexander(text):
        return re.sub(r'\[\[Iron Fist Alexander\|(.+)\]\]', r'[[Alexander|\1]]', text)
    
    def unify_sword_of_st_trina(text):
        return re.sub(r'\[\[Sword of St\. Trina\|(.+)\]\]', r'[[Sword of St Trina|\1]]', text)

    def unify_boc(text):
        return re.sub(r'\[\[Boc the Seamster\|(.+)\]\]', r'[[Boc|\1]]', text)

    def unify_putrid_corpse(text):
        return re.sub(r'\[\[Scarlet Rot Zombie\|(.+)\]\]', r'[[Putrid Corpse|\1]]', text)
    
    def unify_miranda_sprout(text):
        text = re.sub(r'\[\[Poison Flower\|(.+)\]\]', r'[[Miranda Sprout|Miranda Sprout]]', text)
        return re.sub(r'\[\[Miranda Flower\|(.+)\]\]', r'[[Miranda Sprout|Miranda Sprout]]', text)

    def unify_giant_miranda_sprout(text):
        text = re.sub(r'\[\[Giant Poison Flower\|(.+)\]\]', r'[[Giant Miranda Sprout|Giant Miranda Sprout]]', text)
        return re.sub(r'\[\[Giant Miranda Flower\|(.+)\]\]', r'[[Giant Miranda Sprout|Giant Miranda Sprout]]', text)
    
    def unify_shaded_castle(text):
        return re.sub(r'\[\[Shaded Castle\|(.+)\]\]', r'[[The Shaded Castle|\1]]', text)

    def unify_swamp_of_aeonia(text):
        return re.sub(r'\[\[Aeonia Swamp\|(.+)\]\]', r'[[Swamp of Aeonia|\1]]', text)
    
    def unify_stargazers_ruins(text):
        return re.sub(r"\[\[Stargazer\'s Ruins\|(.+)\]\]", r"[[Stargazers' Ruins|Stargazer' Ruins]]", text)
    
    def unify_war_dead_catacombs(text):
        return re.sub(r'\[\[War-[Dd]ead [Cc]atacombs\|(.+)\]\]', r'[[The War-Dead Catacombs|\1]]', text)
    
    def unify_d(text):
        text = re.sub(r'\[\[D\|(.+)\]\]', r'[[D, Hunter of the Dead|\1]]', text)
        return re.sub(r'D Hunter of the Dead', r'D, Hunter of the Dead', text)
    
    def unify_ranni(text):
        # return re.sub(r'\[\[Ranni\|Ranni\]\]', r'[[Ranni the Witch|Ranni the Witch]]', text)
        return re.sub(r'\[\[Ranni the Witch\|(.+)\]\]', r'[[Ranni|\1]]', text)
    
    def unify_enia(text):
        return re.sub(r'\[\[Finger Reader Enia\|(.+)\]\]', r'[[Enia|\1]]', text)
    
    def unify_ensha(text):
        return re.sub(r'\[\[Ensha of the Royal Remains\|(.+)\]\]', r'[[Ensha|\1]]', text)

    def unify_gideon_boss(text):
        return re.sub(r'\[\[Sir Gideon Ofnir, the All-Knowing\|Sir Gideon Ofnir, the All-Knowing\]\]', r'[[Sir Gideon Ofnir, the All-Knowing (Boss)|Sir Gideon Ofnir, the All-Knowing]]', text)
    
    def unify_hewg(text):
        return re.sub(r'Blacksmith Hewg', r'Smithing Master Hewg', text)
    
    def unify_iji(text):
        return re.sub(r'Smithing Master Iji', r'War Counselor Iji', text)
    
    def unify_morgott(text):
        return re.sub(r'Morgott [Tt]he Omen King', r'Morgott, the Omen King', text)
        
    def unify_godfrey(text):
        return re.sub(r'\[\[Hoarah Loux,* Warrior\|(.+)\]\]', r'[[Godfrey, First Elden Lord|\1]]', text)
    
    def unify_gurranq(text):
        return re.sub(r'\[\[Gurranq Beast Clergyman\|(.+)\]\]', r'[[Gurranq, Beast Clergyman|\1]]', text)
    
    def unify_renalla(text):
        text = re.sub(r'\[\[Rennala,* Queen of the Full Moon \(NPC\)\|(.+)\]\]', r'[[Rennala|\1]]', text)
        return re.sub(r'\[\[Rennala,* Queen of the Full Moon\|(.+)\]\]', r'[[Rennala, Queen of the Full Moon|\1]]', text)
    
    def unify_bernahl(text):
        return re.sub(r'\[\[Recusant Bernahl\|(.+)\]\]', r'[[Knight Bernahl|\1]]', text)
    
    def unify_hoslow(text):
        return re.sub(r'\[\[Juno Hoslow\|(.+)\]\]', r'[[Juno Hoslow, Knight of Blood|\1]]', text)
    
    def unify_torrent(text):
        return re.sub(r'\[\[Torrent \(Spirit Steed\)\|(.+)\]\]', r'[[Torrent|\1]]', text)
    
    def unify_moongrum(text):
        return re.sub(r'\[\[Moongrum Carian Knight\|(.+)\]\]', r'[[Moongrum, Carian Knight|\1]]', text)
    
    def unify_imp(text):
        return re.sub(r'\[\[Fanged Imp\|(.+)\]\]', r'[[Imp|Imp]]', text)
    
    def unify_miriel(text):
        return re.sub(r'\[\[Miriel Pastor of Vows\|(.+)\]\]', r'[[Miriel, Pastor of Vows|\1]]', text)
    
    def unify_malenia(text):
        text = re.sub(r'\[\[Malenia\|(.+)\]\]', r'[[Malenia, Blade of Miquella|\1]]', text)
        return re.sub(r'\[\[Malenia Blade of Miquella\|(.+)\]\]', r'[[Malenia, Blade of Miquella|\1]]', text)
        
    def unify_seluvis(text):
        return re.sub(r'\[\[Preceptor Seluvis\|(.+)\]\]', r'[[Seluvis|\1]]', text)
    
    def unify_elphael(text):
        return re.sub(r'\[\[Elphael Brace of the Haligtree\|(.+)\]\]', r'[[Elphael, Brace of the Haligtree|\1]]', text)

    def unify_leyndell(text):
        text = re.sub(r'\[\[Leyndell\|(.+)\]\]', r'[[Leyndell, Royal Capital|\1]]', text)
        text = re.sub(r'\[\[Leyndell[,]* Royal Capital\|(.+)\]\]', r'[[Leyndell, Royal Capital|\1]]', text)
        text = re.sub(r'\[\[Leyndell[,]* Royal Capital \(Legacy Dungeon\)\|(.+)\]\]', r'[[Leyndell, Royal Capital (Legacy Dungeon)|\1]]', text)
        return text
    
    def unify_leyndell_ashen_capital(text):
        return re.sub(r'\[\[Leyndell Ashen Capital\|(.+)\]\]', r'[[Leyndell, Ashen Capital|\1]]', text)
    
    def unify_gelmir(text):
        return re.sub(r'\[\[Mt\. Gelmir\|(.+)\]\]', r'[[Mt Gelmir|\1]]', text)

    def unify_mausoleums(text):
        return re.sub(r'\[\[Walking Mausoleum\|(.+)\]\]', r'[[Wandering Mausoleum|\1]]', text)
    
    def unify_raya_lucaria(text):
        return re.sub(r'\[\[Academy of Raya Lucaria\|(.+)\]\]', r'[[Raya Lucaria Academy|\1]]', text)
    
    def unify_rat(text):
        return re.sub(r'\[\[Rat\|(.+)\]\]', r'[[Giant Rat|\1]]', text)

    def unify_nomadic_merchant_west_liurnia(text):
        text = re.sub(r'\[\[Nomadic Merchant Liurnia of [Tt]he Lakes\|(.+)\]\]', r'[[Nomadic Merchant West Liurnia of the Lakes|\1]]', text)
        return re.sub(r'\[\[Nomadic Merchant West Liurnia of The Lakes\|(.+)\]\]', r'[[Nomadic Merchant West Liurnia of the Lakes|\1]]', text)

    def unify_hermit_merchant_mountaintops_east(text):
        return re.sub(r'\[\[Nomadic Merchant Mountaintops East\|(.+)\]\]', r'[[Hermit Merchant Mountaintops East|Hermit Merchant Mountaintops East]]', text)
    
    def unify_monstrous_crow(text):
        text = re.sub(r'\[\[Giant Crow\|(.+)\]\]', r'[[Monstrous Crow|\1]]', text)
        return re.sub(r'\[\[Monstrous Crow\|(.+)\]\]', r'[[Monstrous Crow|\1]]', text)
    
    def unify_monstrous_dog(text):
        text = re.sub(r'\[\[Giant Dog\|(.+)\]\]', r'[[Monstrous Dog|\1]]', text)
        return re.sub(r'\[\[Monstrous Dog\|(.+)\]\]', r'[[Monstrous Dog|\1]]', text)
    
    def unify_wolf(text):
        return re.sub(r'\[\[Wolf\|(.+)\]\]', r'[[Lone Wolf|\1]]', text)
    
    def unify_kindred(text):
        return re.sub(r'\[\[Lesser Kindred of Rot \(Pests\)\|(.+)\]\]', r'[[Lesser Kindred of Rot|\1]]', text)
    
    def unify_skills(text):
        text = re.sub(r'\[\[Carian Greatsword Skill\|(.+)\]\]', r'[[Carian Greatsword (Skill)|\1]]', text)
        text = re.sub(r'\[\[Parry Skill\|(.+)\]\]', r'[[Parry (Skill)|\1]]', text)
        text = re.sub(r'\[\[Glintstone Pebble Skill\|(.+)\]\]', r'[[Glintstone Pebble (Skill)|\1]]', text)
        return re.sub(r'\[\[Great Oracular Bubble Skill\|(.+)\]\]', r'[[Great Oracular Bubble (Skill)|\1]]', text)
    
    def unify_liurnia(text):
        return re.sub(r'\[\[Liurnia\|(.+)\]\]', r'[[Liurnia of the Lakes|\1]]', text)
    
    def unify_ordina(text):
        return re.sub(r'\[\[Ordina[,]* Liturgical Town\|(.+)\]\]', r'[[Ordina, Liturgical Town|\1]]', text)

    def reformat_notes(text):
        return re.sub(r'\[\[Note:', r'[[Note -', text)

    def unlink_sites_of_grace(text):
        # TODO: This regex overmatches, see Noble's Estoc
        return re.sub(r'\[.+ Site of Grace\]\((.+ Site of Grace)\)', r'\1', text)

    def reify_bullets(text):
        return re.sub(r'%BULLET%', r'*', text)

    def reify_varre_e(text):
        return re.sub(r'%E-LOWERCASE-ACCENTED%', 'é', text) # é

    def applyTargetedCorrections(name, text):
        correction = text

        # Would use match here if Pylance recognized my interpreter as being newer than Python 3.10...
        if name == 'Abandoned Cave':
            correction = re.sub(r' See it on the interactive map by clicking on', r'', text)
        if name == "Alabaster Lord's Sword":
            correction = re.sub(r'Sword\*\*\. ', r'Sword. **', text)
            correction = re.sub(r'drop\. \*\*', r'drop.**', correction)
            correction = re.sub(r'Below shows where.*', r'', correction)
            correction = re.sub(r"Alabaster Lords' Pull", r"Alabaster Lord's Pull", correction)
            correction = Formatter.condense_newlines(correction)
        elif name == 'Anastasia, Tarnished-Eater':
            correction = re.sub(r'\[\[Sacred Scorpion Charm(\|)Sacred Scorpion Charm\]\]', r'[[Sacred Scorpion Charm\|Sacred Scorpion Charm]]', correction)
            correction = re.sub(r'\[\[Butchering Knife(\|)Butchering Knife\]\]', r'[[Butchering Knife\|Butchering Knife]]', correction)
            correction = re.sub(r'\[\[Somber Ancient Dragon Smithing Stone(\|)Somber Ancient Dragon Smithing Stone\]\]', r'[[Somber Ancient Dragon Smithing Stone\|Somber Ancient Dragon Smithing Stone]]', correction)
        elif name == 'Aspects of the Crucible: Horns':
            correction = re.sub(r'\[Ramparts\]\(Ramparts\)', r'Ramparts', text)
        elif name == "Assassin's Crimson Dagger":
            correction = re.sub(r" See Assassin's Crimson Dagger location in the Interactive Map \[here\]\(here\)", r'', text)
        elif name == 'Battle Axe':
            correction = re.sub(r'weapon \n \nCapable', r'weapon*\n\n*Capable', text)
        elif name == 'Beast-Repellent Torch':
            correction = re.sub(r'aroma pacifies wild beasts. Torches', r'aroma pacifies wild beasts.*\n\n*Torches', text)
        elif name == 'Beast Clergyman':
            correction = re.sub(r'\*(.|\n)*Destined Death\.\*', r'', text)
            correction = Formatter.condense_newlines(correction)
        elif name == 'Bloodstained Dagger':
            correction = re.sub(r'#gsc\.tab=0', r'', text)
        elif name == 'Celestial Dew':
            correction = re.sub(r'\[\[Ainsel River\\\|Ainsel River\]\]', r'', correction)
            correction = re.sub(r'\n\n\n\[\[Ainsel River\|Ainsel River\]\]\n', r'', correction)
        elif name == 'Cipher Pata':
            correction = re.sub(r'\[\[Unblockable Blade Skill\|(.+)\]\]', r'[[Unblockable Blade|\1]]', text)
        elif name == 'Crystal Staff':
            correction = re.sub(r'Screenshot.*', r'', text)
        # elif name == 'Cracked Pot':
        #     correction = re.sub(r'vessel', r'bessel', text)
        elif name == 'Cuckoo Greatshield':
            correction = re.sub(r'\[Farming route]\(.+\'Farming route\'\)', r'Farming route', text)
        elif name == "Diallos's Mask":
            correction = re.sub(r' \(\[\[file[^\]]+\]\]\)', r'', text)
        elif name == 'Elden Remembrance':
            correction = re.sub(r'\[Sword Saint Guide\]\(https:\/\/youtu\.be/iJn4mSsa1iM \'Elden Ring Builds#blackflamebushido\'\)', r'', text)
        elif name == 'Fallingstar Beast':
            correction = re.sub(r' \[\[Fallingstar Beast#[^\]]+\]\]', r'', text)
        elif name == 'Fia':
            correction = re.sub(r'\[Sword Saint Guide\]\(https:\/\/youtu\.be/iJn4mSsa1iM \'Elden Ring Builds#blackflamebushido\'\)', r'', text)
        elif name == 'Great Omenkiller Cleaver':
            correction = re.sub(r' \, \.', r'', text)
        elif name == 'Ivory-Draped Tabard':
            correction = re.sub(r'\[Prayer Room\]\(\/Interactive\+Map[^\)]+\)', r'Prayer Room', text)
        elif name == 'Kaiden Set':
            correction = re.sub(r'\[camp\]\(camp\)', r'camp', text)
        elif name in ['Land Octopus', 'Giant Land Octopus']:
            correction = re.sub(r'\[Temple Quarter\]\(\/Interactive[^\)]+\)', r'Temple Quarter', text)
        elif name == 'Malenia, Blade of Miquella':
            correction = re.sub(r'See .*location .*', r'', text)
        elif name == 'Margit, the Fell Omen':
            correction = re.sub(r'\[\[Map Link.*', r'', text)
        elif name == 'Mausoleum Soldier Ashes':
            correction = re.sub(r'\[\[Mausoleum\|Mausoleum\]\]', r'Mausoleum', text)
        elif name == "Miquella's Lily":
            correction = re.sub(r'\[\[Map Link\]\(\/Interactive\+Map\?[^\)]+\)\]', r'', text)
        elif name == 'Royal Greatsword':
            correction = re.sub(r'\/\/Strength', r'Strength', text)
        elif name == 'Flowing Curved Sword':
            correction = re.sub(r' See it on the +\.', r'', text)
        elif name == 'Nox Flowing Sword':
            correction = re.sub(r'\[\[(Flowing Form)', r'[[\1 (Nox Flowing Sword)', text)
        elif name in ['Sorcerer Manchettes', 'Ragged Wolf Set']:
            correction = re.sub(r'\[\[VS ', r'[[', text)
        elif name == "Smithing-Stone Miner's Bell Bearing (3)":
            correction = re.sub(r'\[Click on the image above to enlarge it.*', r'', text)
        elif name == "St. Trina's Arrow":
            correction = re.sub(r' \[Map Link\]\(.+\'\)', r'', text)
        elif name =='Stonesword Key':
            correction = re.sub(r'\* Sold here as shown with the near.*', r'', text)
        elif name == 'Torrent':
            correction = re.sub(r'\[\[Attacking#two\-handing\|two\-hand\]\]', r'two-hand', text)
        elif name == "Troll's Golden Sword":
            correction = re.sub(r'—', r'--', text)
        elif name == 'Volcano Manor':
            correction = re.sub(r'\* (\[\[Diallos.+|\[\[Liurnia of the Lakes.+|\?id.+)', r'', text)
            correction = Formatter.condense_newlines(correction)
        elif name == 'Vulgar Militia Saw':
            correction = re.sub(r'	 \[\[file\/.*', r'', text)
            correction = Formatter.condense_newlines(correction)
        elif name == 'Wakizashi':
            correction = re.sub(r'\n### \n\n', r'', text)
        elif name == 'Zweihander':
            correction = re.sub(r'ä', r'a', text)
        elif name == 'Torch':
            correction = re.sub(r' ### Elden Ring Torch Moveset[\'\,\'\/\(\)\+ \.\|\[\]#\*\w\&\n]*', r'', text)

        return correction

    def section(header, text, separator='\n', mode='cli'):
        f_string = ''

        if mode == 'cli':
            f_string = f'{header}\n--------\n{text}\n{separator}'
        elif mode == 'file':
            f_string = f'{header}\n--------\n{text}\n{separator}'
            
        return f_string
