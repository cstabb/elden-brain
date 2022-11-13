import markdownify as md

class Formatter:
    """
    Formats and cleans text, including targeted corrections.
    """

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