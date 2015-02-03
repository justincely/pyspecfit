from __future__ import print_function

from parser import SpecfitParser

#-------------------------------------------------------------------------------

def check_db_diff(filename1, filename2):
    """Perform a parameter-by-parameter difference

    """

    if isinstance(filename1, str):
        db1 = SpecfitParser(filename1)
    elif isinstance(filename1, SpecfitParser):
        db1 = filename1

    if isinstance(filename2, str):
        db2 = SpecfitParser(filename2)
    elif isinstance(filename2, SpecfitParser):
        db2 = filename2


    assert len(db1) == len(db2), "Databases aren't equal lengths"

    assert set(db1.components.iterkeys()) == set(db2.components.iterkeys()), "Databases don't contain same components"

    n_diff = 0
    for comp1, comp2 in zip(db1, db2):
        for par1, par2 in zip(comp1, comp2):

            if par1.value != par2.value:
                n_diff += 1
                print("{} Value Diff: {} != {}".format(comp1.name, par1.value, par2.value))
            if par1.lower_lim != par2.lower_lim:
                n_diff += 1
                print("{} lower lim Diff: {} != {}".format(comp1.name, par1.lower_lim, par2.lower_lim))
            if par1.upper_lim != par2.upper_lim:
                n_diff += 1
                print("{} upper lim Diff: {} != {}".format(comp1.name, par1.upper_lim, par2.upper_lim))
            if par1.stepsize != par2.stepsize:
                n_diff += 1
                print("{} Stepsize Diff: {} != {}".format(comp1.name, par1.stepsize, par2.stepsize))
            if par1.tolerance != par2.tolerance:
                n_diff += 1
                print("{} Tolerance Diff: {} != {}".format(comp1.name, par1.tolerance, par2.tolerance))

    return n_diff

#-------------------------------------------------------------------------------

def reset_failed_parameters(db, previous_db, write=True, log=None, mode='w'):
    """Set any parameters that hit boundaries to their previous values

    Reset parameters will be kept fixed after being reset.

    Parameters
    ----------
    db : str
        path to the specfit db to reset
    previous_db : str
        path to the specfit db of the previous fitting
    write : bool, opt
        write-out changed db
    log : bool, str
        log file to write the modifications to
    mode : str
        used if a filename is supplied to log, specifies mode to write: a,w

    Returns
    -------
    modified : bool
        has the db been modified and needs to be re-fit?

    """

    current = SpecfitParser(db)
    previous = SpecfitParser(previous_db)
    print("resetting {} to {}".format(db, previous_db))

    failed = 0
    messages = []
    for cur_comp, prev_comp in zip(current, previous):
        for i, (cur_par, prev_par) in enumerate(zip(cur_comp, prev_comp)):
            if cur_par.hit_boundary:

                if (cur_par.value == cur_par.upper_lim == cur_par.lower_lim):
                    continue

                msg =  "{} failed and fixed:  {} --> {} in comp {}, par {}".format(db,
                                                                                   cur_par.value,
                                                                                   prev_par.value,
                                                                                   cur_comp.name,
                                                                                   i+1)
                messages.append(msg + '\n')

                cur_par.value = prev_par.value
                cur_par.fix()
                failed += 1


    if failed:
        #-- Reset all parameters back to previous for the re-fitting
        for cur_comp, prev_comp in zip(current, previous):
            for i, (cur_par, prev_par) in enumerate(zip(cur_comp, prev_comp)):
                if not cur_par.value == prev_par.value:

                    msg =  "{} resetting:  {} --> {} in comp {}, par {}".format(db,
                                                                                cur_par.value,
                                                                                prev_par.value,
                                                                                cur_comp.name,
                                                                                i+1)
                    messages.append(msg + '\n')

                    cur_par.value = prev_par.value

        if log is not None:
            with open(log, mode) as savefile:
                savefile.write(''.join(messages))

        current.write(db)
        return True

    return False
