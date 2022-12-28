from .elden_brain import EldenBrain

import click

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = EldenBrain()

@click.command('list', short_help='List categories/names')
@click.pass_context
@click.option('-c', '--category', multiple=True, default=[], help='The category. Omit to see valid categories.')
def list(ctx, category):
    """
    List all the categories, or, if a category is provided, 
    list all entity names within that category.
    """
    out_list = []
    if not category:
        out_list = ctx.obj.getCategories()
    else:
        for key in category:
            try:
                this_category = ctx.obj.getNamesByCategory(key)[key]
            except KeyError:
                click.echo('Category not recognized, use the list command to see valid categories.')
                return
            if isinstance(this_category, dict):
                for _key, val in this_category.items():
                    out_list += (val)
            else:
                out_list += (this_category)
    out_list.sort()
    click.echo('\n'.join(out_list))

@click.command('create', short_help='Create a local Obsidan Vault from the Elden Ring wiki')
@click.pass_context
@click.argument('name', required=False)
@click.option('-c', '--category', default='', help='The category/directory where the entity will be created. Omit this option to create it in the top-level directory.')
@click.option('-a', '--all', is_flag=True, default=False, help='Create all entities. Ignores other options if used.')
def create(ctx, name, category, all):
    """
    Create a local Obsidian Vault (or individual pages of a Vault) from the Elden Ring wiki.

    Specify a NAME (and an optional category) to create a specific entity, e.g. \'create Dagger -c Weapons\'

    Surround a NAME in quotes to captures names containing spaces and apostrophes.

    Use the --all flag to create all pages. This will take some time.
    """
    if all == True:
        ctx.obj.create()
        return

    if name is not None:
        ctx.obj.create(name, category)
        return
    
    if name is None and category != '':
        ctx.obj.create(category=category)
        return

    click.echo('Options must be provided. Use --all to create all pages.')

def run():
    cli.add_command(list)
    cli.add_command(create)
    cli()

if __name__ == '__main__':
    run()