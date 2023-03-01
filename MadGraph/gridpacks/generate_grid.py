import os

from argparse import ArgumentParser

process_kwargs = dict(
    sixb = dict(
        # the prototype name of the production folder
        prod_proto = "NMSSM_XYH_YToHH_6b_MX_{0}_MY_{1}",
        # 2 - the original files
        template   = "Template/XYH_YToHH_6b",
        ## mX, mY
        points = [
            (450, 300),
            (500, 300),
            (600, 300),
            (600, 400),
            (700, 300),
            (700, 400),
            (700, 500),
            (1000, 300),
            (1000, 700),
            (1200, 300),
            (1200, 700),
            (1200, 1000)
        ]
    ),
    eightb = dict(
        # the prototype name of the production folder
        prod_proto = "NMSSM_XYY_YToHH_8b_MX_{0}_MY_{1}",
        # 2 - the original files
        template   = "Template/XYY_YToHH_8b/",
        ## mX, mY
        points = [
            (500,250),
            (1000,500),
            (1500,500),
            (2000,1000),
            # (mx, my)
            # for mx in range(500, 4000 + 50, 50)
            # for my in range(250, mx//2 + 50, 50)
        ]
    )
)

parser = ArgumentParser()
parser.add_argument('-proc','--process', choices=process_kwargs.keys())
args = parser.parse_args()
kwargs = process_kwargs[args.process]

### things to replace are
### TEMPLATEMH02 [mX]
### TEMPLATEMH03 [mY]

def change_cards(cardname, replacements):
    
    ## first make a backup copy
    bkpname = cardname + '.bak'
    os.system('mv %s %s' % (cardname, bkpname))

    # edit the file
    fin  = open(bkpname, 'r')
    fout = open(cardname, 'w')

    for line in fin:
        for key, rep in replacements.items():
            line = line.replace(key, rep)
        fout.write(line)

    fin.close()
    fout.close()

    ## delete the backup file
    os.system('rm %s' % bkpname)


def do_point(mx, my, prod_proto=None, template=None, **kwargs):
    # 1 - create the folder
    folder = prod_proto.format(mx, my)
    if os.path.isdir(folder):
        print " >> folder", folder, "already existing, forcing its deletion"
        os.system('rm -r %s' % folder)
    os.system('mkdir ' + folder)
    
    # 2 - copy the original files
    template_flrd = template
    
    run_card      = 'run_card.dat'
    proc_card     = 'proc_card.dat'
    # param_card    = 'param_card.dat'
    extramodels   = 'extramodels.dat'
    customizecard = 'customizecards.dat'
    
    # to_copy = [run_card, proc_card, param_card, extramodels, customizecard]
    to_copy = [run_card, proc_card, extramodels, customizecard]

    for tc in to_copy:
        os.system('cp %s/%s %s/%s_%s' % (template_flrd, tc, folder, folder, tc) )

    replacements = {
        'TEMPLATEMH03' : str(mx),
        'TEMPLATEMH02' : str(my),
    }

    # 3 - edit in place the cards
    # change_cards('%s/%s_%s' % (folder, folder, param_card), replacements)
    change_cards('%s/%s_%s' % (folder, folder, customizecard), replacements)
    change_cards('%s/%s_%s' % (folder, folder, proc_card), replacements)


####################################################################################


for p in kwargs['points']:
    print '... generating', p
    do_point(*p, **kwargs)
